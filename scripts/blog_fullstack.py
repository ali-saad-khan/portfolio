"""Full stack articles, appended to POSTS by blog_content.py. Code samples are taken from the
public TaskFlow and Pulseboard repositories."""
import html as _h


def C(s):
    return "<pre><code>" + _h.escape(s.strip("\n"), quote=False) + "</code></pre>"


POSTS = [
    dict(
        slug="optimistic-ui-react-rollback-laravel",
        title="Optimistic UI in React With Rollback (Against a Laravel API)",
        meta="Make a React Kanban board feel instant: apply changes optimistically with a reducer, keep a snapshot and roll back when the Laravel API rejects the request.",
        lead="Waiting for a server round trip before a card moves makes an app feel broken. Optimistic updates fix that, but only if failure is handled properly. Here is the pattern I use, taken from a real React and Laravel project.",
        cover="taskflow", tag="React", read=7,
        related_service="frontend-development", related_case="taskflow-laravel-react-app",
        body="""
<h2>The idea in one paragraph</h2>
<p>When the user drags a card, update the screen immediately, then send the request. If the server says no, put the screen back the way it was and tell the user why. The hard part is not the happy path. It is making the rollback reliable, and making sure the request is actually sent.</p>
<h2>Step 1: make board state a pure reducer</h2>
<p>Optimistic updates are much easier when every change is a plain action applied by a reducer, because the same function that moves a card on screen is easy to unit test. In TaskFlow the board state and actions look like this:</p>
""" + C("""
export interface BoardState {
  phase: "loading" | "ready" | "error";
  error: string | null;
  tasks: Task[];
}

export type BoardAction =
  | { type: "move"; id: number; status: TaskStatus; position: number }
  | { type: "add_pending"; task: Task }
  | { type: "add_confirmed"; tempId: number; task: Task }
  | { type: "remove"; id: number }
  /** Restore a snapshot taken before an optimistic update that the server rejected. */
  | { type: "rollback"; tasks: Task[] };
""") + """
<p>Note the <code>rollback</code> action. It does not try to reverse the change; it simply puts a saved copy of the task list back. Reversing changes one by one is how rollback bugs are born.</p>
<h2>Step 2: one helper for every optimistic call</h2>
<p>Rather than repeat the try/catch in every handler, wrap it once. It takes a snapshot, dispatches the optimistic action, calls the server and restores the snapshot if anything throws:</p>
""" + C("""
async function optimistic<T>(action: BoardAction, call: () => Promise<T>, onOk?: (result: T) => void) {
  const snapshot = stateRef.current.tasks;
  setNotice(null);
  dispatch(action);
  try {
    const result = await call();
    onOk?.(result);
  } catch (e) {
    dispatch({ type: "rollback", tasks: snapshot });
    setNotice(messageOf(e));
  }
}
""") + """
<p>That one-line <code>await call()</code> on its own line is deliberate. My first version wrote <code>onOk?.(await call())</code>. When no callback was passed, optional chaining short-circuited and the server call never ran. The UI moved the card, nothing was saved, and no error appeared. A test caught it, which is a good argument for testing the failure and no-callback paths, not just the success path.</p>
<h2>Step 3: temporary ids for new items</h2>
<p>For creates, the item does not have a server id yet. Add it with a negative temporary id (<code>add_pending</code>), then swap it for the real record when the response arrives (<code>add_confirmed</code>). If the request fails, the same snapshot rollback removes it.</p>
<h2>Step 4: make the failure visible</h2>
<p>A silent rollback looks like a glitch. Show a notice with the server's message. The Laravel API returns one consistent error shape, so the front end can map every failure the same way:</p>
""" + C("""
// Laravel returns: { "message": "...", "code": "validation_failed", "errors": { "title": ["..."] } }
export class ApiError extends Error {
  readonly status: number;
  readonly code: string;
  readonly fieldErrors: Record<string, string[]>;
}
""") + """
<h2>Step 5: test the rollback</h2>
<p>Because the server layer is behind an interface, a test can make the call fail on demand and assert the board returns to its original order. The demo of this project even has a "Simulate network failure" switch so you can watch the rollback happen.</p>
<h2>Limits to be honest about</h2>
<ul>
<li><strong>Overlapping edits.</strong> A snapshot restores the whole list, so if two requests are in flight and the first fails, rolling back can undo the second change too. For heavy concurrent editing you need per-item versions or a queue.</li>
<li><strong>The server stays the source of truth.</strong> The optimistic state is a prediction. When a response arrives, prefer the server's record.</li>
<li><strong>Dialogs that close early.</strong> If the edit dialog closes before the server answers, field-level errors can only appear as a banner. That is a trade-off I documented in the repository.</li>
</ul>
<h2>When not to use it</h2>
<p>Skip optimism for actions that are expensive to undo or that the user must see confirmed, such as payments. For moving a card, reordering a list or toggling a checkbox, it is exactly right.</p>
<p>The full code, including the Laravel API this talks to, is open source in the <a href="/projects/taskflow-laravel-react-app">TaskFlow case study</a>.</p>
""",
    ),
    dict(
        slug="kanban-ordering-laravel-transactions",
        title="Keeping Kanban Card Positions Consistent in Laravel",
        meta="How to reorder cards across columns in Laravel without gaps or duplicates: a TaskOrdering service, contiguous positions, a database transaction and a rollback test.",
        lead="Moving a card between columns looks trivial until two columns need renumbering at once and something fails halfway. This is how I keep positions contiguous in Laravel and prove it with a test.",
        cover="taskflow", tag="Laravel", read=7,
        related_service="rest-api-development", related_case="taskflow-laravel-react-app",
        body="""
<h2>The problem</h2>
<p>A Kanban board stores each task with a <code>status</code> (its column) and a <code>position</code> (its place in the column). Dragging a card to a new column and index means: put it in the new column at that index, shift the cards after it down by one, and close the gap it left behind in the old column. That is several writes, and they must succeed or fail together.</p>
<p>If they do not, you get duplicate positions, gaps, or a card that exists in neither column, and the board looks randomly shuffled after a refresh.</p>
<h2>The rule: positions are always 0 to n-1 per column</h2>
<p>Instead of storing fractional positions or trying to patch numbers, I keep a simple invariant: inside every project and status column, positions are contiguous, starting at zero. To keep it, rebuild the column's order as a list of ids and renumber from that list.</p>
<h2>A small service owns the logic</h2>
""" + C("""
class TaskOrdering
{
    /** Move a task to a column and index. Index is clamped to the column size. */
    public function move(Task $task, TaskStatus $status, int $position): Task
    {
        return DB::transaction(function () use ($task, $status, $position) {
            $oldStatus = $task->status;

            $ids = Task::where('project_id', $task->project_id)
                ->where('status', $status->value)
                ->where('id', '!=', $task->id)
                ->orderBy('position')->orderBy('id')
                ->pluck('id')->all();

            $position = max(0, min($position, count($ids)));
            array_splice($ids, $position, 0, [$task->id]);

            $task->status = $status;
            $task->save();
            $this->renumber($ids);

            if ($oldStatus !== $status) {
                $old = Task::where('project_id', $task->project_id)
                    ->where('status', $oldStatus->value)
                    ->orderBy('position')->orderBy('id')
                    ->pluck('id')->all();
                $this->renumber($old);
            }

            return $task->refresh();
        });
    }
}
""") + """
<p>Three details matter:</p>
<ul>
<li><strong>The whole move is one transaction.</strong> Either both columns are renumbered or neither is.</li>
<li><strong>The index is clamped.</strong> A client that sends position 999 puts the card at the end instead of creating a gap.</li>
<li><strong>Ties are broken by id.</strong> Ordering by <code>position</code> then <code>id</code> keeps the result deterministic even if old data had duplicates.</li>
</ul>
<h2>Validate and authorize before you reorder</h2>
<p>The controller is thin. A Form Request validates <code>status</code> against the enum and <code>position</code> as a non-negative integer, and a Policy makes sure the task belongs to the current user. Bad input returns a 422 with field errors, and someone else's task returns 403, before the service runs.</p>
<h2>Prove the rollback with a test</h2>
<p>The interesting test is the failure case. This one makes the third UPDATE throw, in the middle of renumbering, and asserts that every row is exactly as it was:</p>
""" + C("""
public function test_failed_move_rolls_back_in_a_transaction(): void
{
    $todo = $this->column('todo', 3);
    $this->column('doing', 2);

    // Let the first two UPDATEs succeed, then blow up mid-renumbering.
    $updates = 0;
    DB::listen(function ($query) use (&$updates) {
        if (str_starts_with($query->sql, 'update "tasks"') && ++$updates === 3) {
            throw new \\RuntimeException('boom');
        }
    });

    $before = Task::orderBy('id')->get(['id', 'status', 'position'])->toArray();

    try {
        app(TaskOrdering::class)->move($todo[0], TaskStatus::Doing, 0);
        $this->fail('expected exception');
    } catch (\\RuntimeException $e) {
        $this->assertSame('boom', $e->getMessage());
    }

    $this->assertSame($before, Task::orderBy('id')->get(['id', 'status', 'position'])->toArray());
}
""") + """
<p>Using <code>DB::listen</code> to inject a failure is a handy trick: it proves the transaction boundary really wraps all the writes, without mocking the database.</p>
<h2>Trade-offs</h2>
<ul>
<li><strong>It rewrites rows.</strong> Renumbering updates every card in the affected columns. That is fine for boards with dozens or hundreds of cards. For very large lists, use fractional or lexicographic ranks (as some tools do) and rebalance occasionally.</li>
<li><strong>Concurrent moves.</strong> Two users moving cards in the same column at once can interleave. If that matters, lock the project's tasks with <code>lockForUpdate()</code> inside the transaction.</li>
</ul>
<p>The whole API, 36 feature tests and a React front end are in the open-source <a href="/projects/taskflow-laravel-react-app">TaskFlow case study</a>.</p>
""",
    ),
    dict(
        slug="accessible-sortable-table-react",
        title="Building an Accessible, Sortable Data Table in React",
        meta="Make a React data table usable with a keyboard and a screen reader: real table markup, aria-sort on headers, labelled filters, live-region counts and a chart text alternative.",
        lead="Most dashboards ship a sortable table that works with a mouse and little else. Here are the specific details I use to make one that works with a keyboard and assistive technology, with the code from my Pulseboard dashboard.",
        cover="pulseboard", tag="React", read=6,
        related_service="frontend-development", related_case="pulseboard-react-dashboard",
        body="""
<h2>Start with real table markup</h2>
<p>A <code>&lt;table&gt;</code> with <code>&lt;th scope="col"&gt;</code> headers already gives screen readers row and column navigation. Replacing it with divs and then trying to rebuild that with ARIA is more work and usually worse. Add a caption that is hidden visually but announced:</p>
""" + C("""
<table className="w-full min-w-[640px] text-sm">
  <caption className="sr-only">Orders</caption>
  <thead>
    <tr>
      <th scope="col">Order</th>
      ...
""") + """
<h2>Sortable headers: a button inside the th, plus aria-sort</h2>
<p>Do not put a click handler on the <code>&lt;th&gt;</code> itself. Put a real <code>&lt;button&gt;</code> inside it so it is focusable and works with Enter and Space, and set <code>aria-sort</code> on the header so assistive tech announces the current sort:</p>
""" + C("""
const th = (k: SortKey, label: string) => (
  <th
    scope="col"
    aria-sort={sortKey === k ? (dir === "asc" ? "ascending" : "descending") : "none"}
  >
    <button type="button" onClick={() => onSort(k)}>
      {label} {sortKey === k ? (dir === "asc" ? "▲" : "▼") : ""}
    </button>
  </th>
);
""") + """
<p>The arrow is a visual cue only. The truth for screen readers is in <code>aria-sort</code>, so the two never disagree.</p>
<h2>Label every filter, even the ones without visible labels</h2>
<p>A search box with only a placeholder has no accessible name. If your design hides the label, use a visually hidden one:</p>
""" + C("""
<label className="sr-only" htmlFor="q">Search orders</label>
<input id="q" type="search" placeholder="Search customer or order ID" ... />
""") + """
<p>The same goes for the status and region selects. A placeholder is not a label.</p>
<h2>Announce results without stealing focus</h2>
<p>When the user types in the search box and the table shrinks, a sighted user sees it happen. A screen reader user hears nothing unless you tell them. A polite live region reports the new count without moving focus:</p>
""" + C("""
<span aria-live="polite">{sorted.length} orders · page {current + 1} of {pages}</span>
""") + """
<h2>Do not rely on colour alone</h2>
<p>Status badges are green, amber and red, but each one also contains its status as text (<code>paid</code>, <code>pending</code>, <code>refunded</code>). Someone who cannot distinguish the colours still gets the meaning.</p>
<h2>Give the chart a text alternative</h2>
<p>A chart drawn as SVG is just a picture to a screen reader. Give it a role and a label, and include the same data as hidden text:</p>
""" + C("""
<svg viewBox="0 0 100 48" role="img" aria-label={`Weekly revenue, ${data.length} weeks`}>
  ...
</svg>
<figcaption className="sr-only">
  {data.map((d) => `Week of ${d.label}: ${format(d.value)}`).join("; ")}
</figcaption>
""") + """
<h2>Test the behaviour, not just the pixels</h2>
<p>Accessible behaviour is easy to break by accident, so I test it. With Testing Library you can find the header by its role and assert the sort state changes:</p>
""" + C("""
const th = screen.getByRole("columnheader", { name: /Amount/ });
await userEvent.click(within(th).getByRole("button"));
expect(th).toHaveAttribute("aria-sort", "descending");
await userEvent.click(within(th).getByRole("button"));
expect(th).toHaveAttribute("aria-sort", "ascending");
""") + """
<h2>What this does not cover</h2>
<p>This checklist covers the structure and semantics, which is the part developers can fix in code. It is not a full accessibility audit. I have not run screen-reader testing on this demo, so treat it as a solid baseline and run your own assistive-technology checks before calling a product accessible.</p>
<p>See the working dashboard and its source in the <a href="/projects/pulseboard-react-dashboard">Pulseboard case study</a>.</p>
""",
    ),
    dict(
        slug="react-api-adapters-mock-laravel",
        title="One Typed API Interface, Two Adapters: Developing React Against a Mock or Laravel",
        meta="Define a single TypeScript Api interface with an HTTP adapter for Laravel and an in-memory mock, run one contract test suite against both, and ship a static demo.",
        lead="If your React components call fetch directly, you cannot demo the app without a server and you cannot test it without mocking the network. A typed interface with swappable adapters solves both. Here is the structure from my TaskFlow project.",
        cover="taskflow", tag="Architecture", read=7,
        related_service="frontend-development", related_case="taskflow-laravel-react-app",
        body="""
<h2>The problem with calling fetch in components</h2>
<p>When components talk to the network directly, three things get hard: running the UI without a backend (for demos, design work or CI), testing it without mocking <code>fetch</code> everywhere, and keeping the front end's idea of the API in sync with the real one.</p>
<h2>Step 1: define the surface once</h2>
<p>Describe everything the UI needs from the server as one TypeScript interface. The components only ever import this interface:</p>
""" + C("""
export interface Api {
  readonly mode: "http" | "mock";
  auth: {
    login(input: LoginInput): Promise<AuthResult>;
    logout(): Promise<void>;
    me(): Promise<User>;
  };
  projects: {
    list(): Promise<Project[]>;
    create(input: ProjectInput): Promise<Project>;
    remove(id: number): Promise<void>;
  };
  tasks: {
    list(projectId: number): Promise<Task[]>;
    create(projectId: number, input: TaskInput): Promise<Task>;
    move(id: number, input: MoveInput): Promise<Task>;
  };
}
""") + """
<h2>Step 2: two implementations</h2>
<p>The <strong>HTTP adapter</strong> talks to the real Laravel API and turns its uniform error shape into a typed <code>ApiError</code>. The <strong>mock adapter</strong> keeps everything in memory (and in <code>localStorage</code> for a demo), simulates latency, and enforces the same rules: 401 when not signed in, 422 with field errors for bad input, 404 for missing records.</p>
<h2>Step 3: choose at build time</h2>
<p>A build-time environment variable picks the adapter. Because it is a direct comparison, the bundler removes the one you did not select:</p>
""" + C("""
export const api: Api =
  import.meta.env.VITE_API_MODE === "mock"
    ? createMockAdapter()
    : createHttpAdapter({ baseUrl: import.meta.env.VITE_API_URL ?? "http://localhost:8000/api/v1" });
""") + """
<p>That is how the same React code produces a static demo (mock adapter, no server needed) and a production build (HTTP adapter, real Laravel API).</p>
<h2>Step 4: one contract test suite, run against every adapter</h2>
<p>The risk with a mock is that it drifts from the real thing. To limit that, write the behaviour you expect once, as a function that takes an adapter factory, and run it against each implementation:</p>
""" + C("""
export function runApiContract(name: string, factory: () => Api) {
  describe(`Api contract: ${name}`, () => {
    it("rejects unauthenticated calls with 401", async () => {
      expect((await rejects(api.projects.list())).status).toBe(401);
    });
    // login, validation errors, ownership, move/reorder behaviour ...
  });
}

runApiContract("mockAdapter", () => createMockAdapter());
""") + """
<p>The same file can be pointed at the HTTP adapter against a running test server. In this project the HTTP adapter has its own tests with a stubbed <code>fetch</code>, and I only smoke-tested it by hand against a live Laravel server. I would not claim more than that.</p>
<h2>What you gain</h2>
<ul>
<li><strong>A deployable demo with no backend.</strong> Useful for a portfolio, a design review or a quick stakeholder preview.</li>
<li><strong>Fast, deterministic UI tests.</strong> No network, no flaky timing.</li>
<li><strong>A written contract.</strong> The interface and its shared tests document what the API promises.</li>
<li><strong>Room to change backends.</strong> Swapping Laravel for another service means writing one adapter.</li>
</ul>
<h2>What it costs</h2>
<p>You maintain a mock. Keep it small, keep it honest about errors, and make the contract tests the thing that stops it drifting. Do not let the mock become a second implementation of your business rules; if it needs complex logic, that logic probably belongs behind the real API.</p>
<p>The complete project, a Laravel 12 API plus the React app, is in the <a href="/projects/taskflow-laravel-react-app">TaskFlow case study</a>, with a live demo running on the mock adapter.</p>
""",
    ),
]
