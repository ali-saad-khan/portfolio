"""Original blog articles written for saadconsulting.tech. Body is trusted HTML."""

POSTS = [
{
 "slug": "idempotent-payment-webhooks-laravel",
 "title": "How to Handle Payment Webhooks in Laravel Without Double-Processing",
 "meta": "Payment gateways retry webhooks, so handlers must be idempotent. Verify signatures, store event IDs under a unique index and process inside one transaction.",
 "lead": "Payment gateways deliver webhooks at least once, not exactly once. If your handler credits an order every time it is called, a retry means a double credit. Here is a pattern that stays correct.",
 "cover": "payment-gateways", "tag": "Payments", "read": 6,
 "related_service": "payment-gateway-integration", "related_case": "payment-gateway-integrations",
 "body": """
<h2>Why webhooks arrive more than once</h2>
<p>Most gateways retry a webhook when your server does not answer with a 2xx status quickly enough. Network timeouts, a deploy in the middle of a request, or a slow database can all make a successful delivery look like a failure to the sender. The sender then tries again, so your code sees the same event two or three times. Treat duplicates as normal, not as an edge case.</p>
<h2>Step 1: verify the signature</h2>
<p>Never trust a webhook just because it hits your URL. Compute the HMAC of the <strong>raw</strong> request body with your signing secret and compare it in constant time. Read the raw body, not re-encoded JSON, because re-encoding can change the bytes.</p>
<pre><code>$payload   = $request-&gt;getContent();
$signature = (string) $request-&gt;header('X-Signature');
$expected  = hash_hmac('sha256', $payload, config('services.gateway.secret'));

abort_unless(hash_equals($expected, $signature), 401);</code></pre>
<p>The header name and hashing scheme differ per gateway, so follow your provider's documentation. The shape of the check stays the same.</p>
<h2>Step 2: record the event ID under a unique index</h2>
<p>Create a table that stores every processed event ID and put a <strong>unique index</strong> on it. The database, not your application code, then guarantees that an event is only accepted once, even when two requests arrive at the same moment.</p>
<pre><code>Schema::create('webhook_events', function (Blueprint $table) {
    $table-&gt;id();
    $table-&gt;string('provider_event_id')-&gt;unique();
    $table-&gt;string('type');
    $table-&gt;timestamps();
});</code></pre>
<p>A check like "if the event exists, skip it" followed by an insert is not safe on its own. Two parallel requests can both pass the check. The unique index closes that gap.</p>
<h2>Step 3: process and record in one transaction</h2>
<pre><code>try {
    DB::transaction(function () use ($event) {
        WebhookEvent::create([
            'provider_event_id' =&gt; $event['id'],
            'type'              =&gt; $event['type'],
        ]);

        $this-&gt;applyEvent($event); // mark order paid, credit wallet, etc.
    });
} catch (UniqueConstraintViolationException $e) {
    // Already handled. Fall through and return 2xx.
}

return response()-&gt;noContent();</code></pre>
<p><code>UniqueConstraintViolationException</code> is available in current Laravel versions. On older ones, catch <code>QueryException</code> and check the error code. Because the event row and the business change commit together, a crash halfway through leaves neither behind, and the gateway's next retry processes the event cleanly.</p>
<h2>Step 4: answer fast, work later if needed</h2>
<p>Return a 2xx response as soon as the event is safely stored. If the real work is slow, such as sending emails or calling other APIs, dispatch a queued job from inside the handler and let the queue worker do it. Make that job idempotent too, since queues can also run a job twice.</p>
<h2>Also handle out-of-order events</h2>
<p>Events can arrive in a different order than they happened. Do not assume <code>payment.succeeded</code> always arrives after <code>payment.created</code>. Compare the state you hold with the state the event implies, and ignore events that would move an order backwards.</p>
<h2>Checklist</h2>
<ul class="check-list">
<li>Signature verified against the raw body, with a constant-time compare</li>
<li>Event ID stored under a unique database index</li>
<li>Business change and event record committed in one transaction</li>
<li>2xx returned quickly, slow work moved to idempotent queued jobs</li>
<li>A test that sends the same event twice and asserts a single credit</li>
</ul>
<p>That last test is the cheapest insurance you can buy. If you want payment flows built and tested this way, see my <a href="/services/payment-gateway-integration">payment gateway integration service</a> or the <a href="/projects/payment-gateway-integrations">payment integrations case study</a>.</p>
"""
},
{
 "slug": "wallet-ledger-design-mysql-laravel",
 "title": "Designing a Wallet Ledger in MySQL and Laravel: Integers, Transactions and Locks",
 "meta": "How to design a safe wallet ledger: store money as integers, write append-only entries, lock rows inside transactions and reconcile balances with tests.",
 "lead": "A wallet is a ledger problem, not a CRUD problem. The rules that keep it correct are simple, but skipping any one of them leads to lost or duplicated money.",
 "cover": "database-schema", "tag": "Database", "read": 7,
 "related_service": "database-engineering", "related_case": "fincore-wallet-ledger-api",
 "body": """
<h2>Rule 1: store money as integers</h2>
<p>Floating-point numbers cannot represent most decimal amounts exactly, so <code>0.1 + 0.2</code> is not <code>0.3</code>. Store the smallest currency unit as an integer (cents, paisa) in a <code>BIGINT</code> column, and keep the currency code next to it. Convert to a display format only at the edge of your system.</p>
<pre><code>$table-&gt;bigInteger('amount');          // minor units, e.g. 1050 = 10.50
$table-&gt;char('currency', 3);           // ISO 4217 code</code></pre>
<h2>Rule 2: write entries, do not edit balances</h2>
<p>Instead of updating a number in place, append immutable ledger entries: a debit or a credit with an amount, a reason and a reference. The balance is the sum of entries. That gives you a full audit trail and lets you explain any balance by listing the rows behind it.</p>
<p>For performance you can keep a cached <code>balance</code> column on the wallet, but treat it as a derived value that must always equal the sum of the entries, and verify that in tests and in a periodic reconciliation job.</p>
<h2>Rule 3: lock the wallet inside a transaction</h2>
<p>Two simultaneous withdrawals can both read the same balance, both see enough funds, and both succeed. Prevent that by locking the wallet row for the duration of the transaction.</p>
<pre><code>DB::transaction(function () use ($walletId, $amount, $reference) {
    $wallet = Wallet::whereKey($walletId)-&gt;lockForUpdate()-&gt;firstOrFail();

    if ($wallet-&gt;balance &lt; $amount) {
        throw new InsufficientFunds();
    }

    LedgerEntry::create([
        'wallet_id' =&gt; $wallet-&gt;id,
        'type'      =&gt; 'debit',
        'amount'    =&gt; $amount,
        'reference' =&gt; $reference,   // unique, see below
    ]);

    $wallet-&gt;decrement('balance', $amount);
});</code></pre>
<p><code>lockForUpdate()</code> only works inside a transaction, and it needs an InnoDB table. When a transfer touches two wallets, always lock them in the same order, for example by ascending ID, to avoid deadlocks.</p>
<h2>Rule 4: make every operation idempotent</h2>
<p>Clients retry requests, and a retry must not move money twice. Require an idempotency key or unique reference per operation, put a unique index on it, and return the original result if the key was already used.</p>
<pre><code>$table-&gt;string('reference')-&gt;unique();</code></pre>
<h2>Rule 5: keep the database honest</h2>
<p>Application checks can be bypassed by a bug. Add constraints so the database refuses bad data: foreign keys from entries to wallets, a unique reference, and a <code>CHECK</code> that amounts are positive where your MySQL version enforces it.</p>
<h2>Test the invariants, not just the happy path</h2>
<ul class="check-list">
<li>The balance equals the sum of entries after any sequence of operations</li>
<li>A withdrawal larger than the balance is rejected and changes nothing</li>
<li>Sending the same reference twice results in one entry</li>
<li>Concurrent withdrawals cannot overdraw the wallet</li>
</ul>
<p>My open-source <a href="/projects/fincore-wallet-ledger-api">FinCore wallet and ledger API</a> is a worked example of these ideas with tests, and the <a href="/services/database-engineering">database engineering service</a> covers schema design for this kind of system.</p>
"""
},
{
 "slug": "laravel-rest-api-design-checklist",
 "title": "A Practical Checklist for Designing a Laravel REST API",
 "meta": "A practical Laravel REST API checklist: versioning, validation, consistent errors, pagination, rate limiting, authentication, idempotency and tests.",
 "lead": "Good APIs feel boring to use: predictable URLs, predictable errors, predictable pagination. This is the checklist I run through before an API goes to production.",
 "cover": "rest-api", "tag": "APIs", "read": 6,
 "related_service": "rest-api-development", "related_case": "fincore-wallet-ledger-api",
 "body": """
<h2>1. Version from day one</h2>
<p>Put the version in the path, such as <code>/api/v1/orders</code>. Changing a response shape later is painful for existing clients, and a version prefix gives you room to do it without breaking anyone.</p>
<h2>2. Validate input with Form Requests</h2>
<p>Keep validation out of controllers. A Form Request class holds the rules, authorizes the caller, and returns a 422 response with field-level errors automatically.</p>
<pre><code>public function rules(): array
{
    return [
        'email'  =&gt; ['required', 'email'],
        'amount' =&gt; ['required', 'integer', 'min:1'],
    ];
}</code></pre>
<h2>3. Shape output with API Resources</h2>
<p>Return data through Eloquent API Resources rather than raw models. You control exactly which fields are exposed, so adding a column to a table never leaks it into the API by accident.</p>
<h2>4. Use one error format everywhere</h2>
<p>Clients should not have to guess how errors look. Pick a single structure and use it for validation errors, authentication failures and server errors alike, with correct HTTP status codes: 400 or 422 for bad input, 401 for unauthenticated, 403 for forbidden, 404 for missing, 409 for conflicts, 429 for rate limits.</p>
<pre><code>{
  "message": "The given data was invalid.",
  "errors": { "amount": ["The amount must be at least 1."] }
}</code></pre>
<h2>5. Paginate every list</h2>
<p>An endpoint that returns "all orders" works in development and falls over in production. Use <code>paginate()</code> or cursor pagination for large, fast-changing data, and cap the page size on the server.</p>
<h2>6. Authenticate and authorize deliberately</h2>
<p>Laravel Sanctum covers token authentication for most first-party and mobile clients. Authentication says who the caller is; policies decide what they may do. Check ownership on every resource lookup so one user can never fetch another user's record by changing an ID.</p>
<h2>7. Rate limit</h2>
<p>Apply the built-in throttle middleware, with stricter limits on login and other sensitive endpoints. Return the standard 429 status so clients can back off.</p>
<h2>8. Make unsafe retries safe</h2>
<p>For operations that create things or move money, accept an <code>Idempotency-Key</code> header and store it under a unique index, so a client retry returns the first result instead of repeating the action. The same idea is covered in my post on <a href="/blog/idempotent-payment-webhooks-laravel">payment webhooks</a>.</p>
<h2>9. Avoid N+1 queries in resources</h2>
<p>Resources that touch relationships can trigger one query per row. Eager load with <code>with()</code> in the controller. See <a href="/blog/fix-n-plus-one-queries-laravel">how to find and fix N+1 queries</a>.</p>
<h2>10. Write feature tests for the contract</h2>
<ul class="check-list">
<li>Happy path returns the documented status and JSON shape</li>
<li>Invalid input returns 422 with field errors</li>
<li>Unauthenticated and unauthorized calls are rejected</li>
<li>Another user's resource returns 403 or 404</li>
</ul>
<p>Need an API built to this standard? Have a look at the <a href="/services/rest-api-development">REST API development service</a>.</p>
"""
},
{
 "slug": "fix-n-plus-one-queries-laravel",
 "title": "How to Find and Fix N+1 Queries in Laravel",
 "meta": "N+1 queries silently slow Laravel apps. Learn how to spot them, fix them with eager loading and withCount, and block them in development.",
 "lead": "A page that runs fine with ten rows and crawls with ten thousand is often an N+1 problem. It is one of the most common causes of slow Laravel pages, and one of the easiest to fix.",
 "cover": "laravel-code", "tag": "Performance", "read": 5,
 "related_service": "production-debugging", "related_case": "enterprise-wordpress-revamp",
 "body": """
<h2>What an N+1 query looks like</h2>
<p>You load a list of records with one query, then access a relationship on each one. Each access runs another query, so a list of 100 posts triggers 1 + 100 queries.</p>
<pre><code>$posts = Post::all();               // 1 query

foreach ($posts as $post) {
    echo $post-&gt;author-&gt;name;        // 1 query per post
}</code></pre>
<h2>Fix 1: eager load with with()</h2>
<p>Tell Eloquent up front which relationships you need. It loads them in one extra query instead of one per row.</p>
<pre><code>$posts = Post::with('author')-&gt;get();   // 2 queries total</code></pre>
<p>Nested relationships work too: <code>with('author.company')</code>. You can also select only the columns you need, for example <code>with('author:id,name')</code>, making sure to include the key columns Eloquent needs to match rows.</p>
<h2>Fix 2: use withCount for totals</h2>
<p>If you only need a count, do not load every related row just to count it in PHP.</p>
<pre><code>$posts = Post::withCount('comments')-&gt;get();
// $post-&gt;comments_count</code></pre>
<h2>Fix 3: block lazy loading in development</h2>
<p>The best fix is making the mistake loud. Laravel can throw an exception whenever a relationship is lazy loaded, so N+1 bugs fail in development instead of reaching production.</p>
<pre><code>// AppServiceProvider::boot()
Model::preventLazyLoading(! $this-&gt;app-&gt;isProduction());</code></pre>
<h2>How to spot them</h2>
<ul class="check-list">
<li>Laravel Debugbar or Telescope in development shows query counts per request</li>
<li><code>DB::listen()</code> or the query log can print every query in a test</li>
<li>A query count that grows with the number of rows is the telltale sign</li>
<li>Slow-query logging on MySQL catches the worst offenders in production</li>
</ul>
<h2>Other quick wins</h2>
<p>Add indexes on columns you filter and join on, paginate instead of loading everything, and use <code>chunkById()</code> for large batch jobs so you never hold a whole table in memory. Measure before and after, because the right fix depends on where the time is actually spent.</p>
<p>If an application has become slow and you need someone to track down why, that is what my <a href="/services/production-debugging">production debugging and maintenance</a> service is for.</p>
"""
},
{
 "slug": "how-to-hire-a-laravel-developer",
 "title": "How to Hire a Freelance Laravel Developer: What to Check Before You Commit",
 "meta": "Hiring a freelance Laravel developer? Check for real code, tests, payment and security experience, clear communication and a sensible scope before you start.",
 "lead": "Plenty of developers can make a Laravel page work. Fewer can build something that stays correct as it grows. These are the checks that separate the two.",
 "cover": "about", "tag": "Hiring", "read": 5,
 "related_service": "laravel-development", "related_case": "practical-meal-subscription-backend",
 "body": """
<h2>1. Ask to see real code</h2>
<p>A portfolio of screenshots tells you little about a backend. Look for public repositories or detailed case studies. Read how the code is organised, whether there are tests, and whether the README explains the design decisions. If client work is private, a good developer can still describe the problem and approach without revealing anything confidential.</p>
<h2>2. Check for tests</h2>
<p>Tests are the cheapest signal of care. A developer who writes feature tests for money, permissions and validation will usually produce fewer surprises after launch. Ask how they test and what they consider essential to cover.</p>
<h2>3. Look for experience with your type of problem</h2>
<p>Laravel covers a lot of ground. Payment integrations, subscriptions and billing logic, multi-role permissions, REST APIs for mobile apps and heavy reporting all call for different instincts. Ask for an example close to what you need and how they handled the tricky part.</p>
<h2>4. Ask about security basics</h2>
<ul class="check-list">
<li>How do they validate input and authorize access to each record?</li>
<li>How do they store secrets and avoid committing them to the repository?</li>
<li>How do they handle passwords, tokens and webhook signatures?</li>
</ul>
<p>You are not looking for a lecture. You are looking for specific, confident answers.</p>
<h2>5. Judge communication early</h2>
<p>The first few messages predict the whole project. Good signs are clarifying questions, plain language, and honest notes about risks or unknowns. Be cautious about instant, unqualified promises on timeline and price before anyone has understood the scope.</p>
<h2>6. Agree on scope and milestones</h2>
<p>Break the work into milestones you can review, each with a clear outcome. Agree what is included, what counts as a change, and how you will communicate. Small, frequent deliveries expose misunderstandings while they are still cheap to fix.</p>
<h2>7. Make sure you own the result</h2>
<p>Settle before work starts that the code lives in a repository you control, that deployment and access details are documented, and that you can hand the project to someone else later. Good work should never lock you in.</p>
<h2>8. Plan for after launch</h2>
<p>Software needs maintenance: updates, monitoring and the occasional production issue. Ask how fixes and ongoing support are handled so you are not searching for help in the middle of an incident.</p>
<h2>Working with me</h2>
<p>I am a freelance Laravel and PHP developer based in Karachi, working remotely with clients worldwide. You can see my <a href="/projects">case studies and open-source code</a>, read about <a href="/services/laravel-development">Laravel development</a>, or <a href="/contact">send me a short description of your project</a> and I will reply by email.</p>
"""
},
]
