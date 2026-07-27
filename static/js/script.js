/* =============================================================
   script.js — Friendly Compiler frontend logic
   ============================================================= */

document.addEventListener('DOMContentLoaded', () => {

    // ── Starter code snippets ──────────────────────────────────
    const snippets = {
        c: `// ✅ Sample C program with intentional errors — try running it!
#include <stdio.h>

int main() {
    int x = 5       // ← missing semicolon
    int y = 10;

    printf("Sum is: %d\\n", add(x, y));

    return 0;
}

// Function declared AFTER main — also missing return
int add(int a, int b) {
    int sum = a + b;
    // ← no return statement!
}
`,
        java: `// ✅ Sample Java program with intentional errors — try running it!
public class Main {
    public static void main(String[] args) {
        int x = 5       // ← missing semicolon
        int y = 10;

        System.out.println("Sum is: " + add(x, y));
    }

    // Missing return statement below
    public static int add(int a, int b) {
        int sum = a + b;
        // ← no return statement!
    }
}
`
    };

    const tipsData = {
        c: [
            'Every statement ends with <code>;</code>',
            'Declare variables with a type: <code>int x = 5;</code>',
            'Include headers: <code>#include &lt;stdio.h&gt;</code>',
            'Match every <code>{</code> with a <code>}</code>',
            'Functions must have a <code>return</code> if non-void',
        ],
        java: [
            'Every statement ends with <code>;</code>',
            'Declare variables: <code>int x = 5;</code>',
            'The class name must match the filename',
            'Import classes: <code>import java.util.Scanner;</code>',
            'Non-void methods need a <code>return</code> statement',
        ]
    };

    // ── DOM refs ───────────────────────────────────────────────
    const codeEditorEl   = document.getElementById('code-editor');
    const runBtn         = document.getElementById('run-btn');
    const clearBtn       = document.getElementById('clear-btn');
    const resetBtn       = document.getElementById('reset-btn');
    const themeBtn       = document.getElementById('theme-btn');
    const sidebarIcons   = document.querySelectorAll('.sidebar-icon[data-lang]');
    const fileNameTab    = document.getElementById('file-name-tab');
    const langSubtitle   = document.getElementById('lang-subtitle');
    const badgeText      = document.getElementById('badge-text');
    const outputStatus   = document.getElementById('output-status');
    const welcomeScreen  = document.getElementById('welcome-screen');
    const outputRendered = document.getElementById('output-rendered');
    const tipsList       = document.getElementById('tips-list');
    const iconSun        = themeBtn.querySelector('.icon-sun');
    const iconMoon       = themeBtn.querySelector('.icon-moon');

    // ── CodeMirror ────────────────────────────────────────────
    const editor = CodeMirror.fromTextArea(codeEditorEl, {
        lineNumbers:      true,
        mode:             'text/x-csrc',
        theme:            'default',
        matchBrackets:    true,
        autoCloseBrackets:true,
        indentUnit:       4,
        tabSize:          4,
        lineWrapping:     true,
        extraKeys: {
            'Ctrl-Enter': () => runBtn.click(),
            'Cmd-Enter':  () => runBtn.click(),
        }
    });

    // ── State ─────────────────────────────────────────────────
    let currentLang = 'c';
    let isDark      = false;

    // Initialise editor with C snippet
    editor.setValue(snippets[currentLang]);
    renderTips(currentLang);

    // ── Language switching ────────────────────────────────────
    sidebarIcons.forEach(icon => {
        icon.addEventListener('click', () => {
            const lang = icon.getAttribute('data-lang');
            if (lang === currentLang) return;

            currentLang = lang;

            // Update sidebar active state
            sidebarIcons.forEach(i => i.classList.remove('active'));
            icon.classList.add('active');

            // Update body class for language-specific colour accents
            document.body.classList.toggle('lang-java', lang === 'java');

            // Update header info
            if (lang === 'java') {
                fileNameTab.innerHTML = `<svg viewBox="0 0 16 16" width="12" height="12" fill="currentColor" style="margin-right:5px"><path d="M4 1h5l3 3v10a1 1 0 01-1 1H4a1 1 0 01-1-1V2a1 1 0 011-1zm4.5 0v3H12"/></svg>Main.java`;
                langSubtitle.textContent = 'Java Language';
                badgeText.textContent   = 'Java Compiler';
            } else {
                fileNameTab.innerHTML = `<svg viewBox="0 0 16 16" width="12" height="12" fill="currentColor" style="margin-right:5px"><path d="M4 1h5l3 3v10a1 1 0 01-1 1H4a1 1 0 01-1-1V2a1 1 0 011-1zm4.5 0v3H12"/></svg>main.c`;
                langSubtitle.textContent = 'C Language';
                badgeText.textContent   = 'C Compiler';
            }

            // Switch CodeMirror mode
            editor.setOption('mode', lang === 'java' ? 'text/x-java' : 'text/x-csrc');
            editor.setValue(snippets[lang]);

            // Reset output to welcome screen
            showWelcome();

            // Update tips
            renderTips(lang);
        });
    });

    // ── Theme toggle ──────────────────────────────────────────
    themeBtn.addEventListener('click', () => {
        isDark = !isDark;
        document.body.classList.toggle('dark-theme', isDark);
        editor.setOption('theme', isDark ? 'darcula' : 'default');
        iconSun.style.display  = isDark ? 'none'  : '';
        iconMoon.style.display = isDark ? ''      : 'none';
    });

    // ── Reset to sample ───────────────────────────────────────
    resetBtn.addEventListener('click', () => {
        editor.setValue(snippets[currentLang]);
        showWelcome();
    });

    // ── Clear output ──────────────────────────────────────────
    clearBtn.addEventListener('click', showWelcome);

    // ── Run / Compile ─────────────────────────────────────────
    runBtn.addEventListener('click', async () => {
        const code = editor.getValue();
        if (!code.trim()) {
            showOutput([{ type: 'warning', title: 'Empty Editor', body: 'Please write some code before clicking Run.' }], false);
            return;
        }

        // Show loading state
        setLoading(true);
        showLoadingShimmer();

        try {
            const response = await fetch('/compile', {
                method:  'POST',
                headers: { 'Content-Type': 'application/json' },
                body:    JSON.stringify({ code, language: currentLang })
            });

            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }

            const data = await response.json();
            renderCompilerOutput(data.output || '', data.success);

        } catch (err) {
            showOutput([{
                type:  'error',
                title: 'Connection Error',
                body:  `Could not reach the server.\n${err.message}`
            }], false);
        } finally {
            setLoading(false);
        }
    });

    // ── Helpers ───────────────────────────────────────────────

    function setLoading(on) {
        runBtn.disabled = on;
        runBtn.classList.toggle('loading', on);
        if (on) {
            runBtn.innerHTML = `
                <svg style="animation:spin 0.8s linear infinite" viewBox="0 0 24 24" width="14" height="14" fill="currentColor">
                  <path d="M12 2v4c-3.31 0-6 2.69-6 6s2.69 6 6 6 6-2.69 6-6h4c0 5.52-4.48 10-10 10S2 17.52 2 12 6.48 2 12 2z"/>
                </svg> Compiling…`;
        } else {
            runBtn.innerHTML = `<svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor"><path d="M8 5v14l11-7z"/></svg> Run`;
        }
    }

    function showWelcome() {
        welcomeScreen.style.display  = 'flex';
        outputRendered.style.display = 'none';
        outputRendered.innerHTML     = '';
        outputStatus.className       = 'output-status';
        outputStatus.textContent     = '';
    }

    function showLoadingShimmer() {
        welcomeScreen.style.display  = 'none';
        outputRendered.style.display = 'block';
        outputRendered.innerHTML = `
            <div class="loading-shimmer">
                <div class="shimmer-line short"></div>
                <div class="shimmer-line long"></div>
                <div class="shimmer-line medium"></div>
                <div class="shimmer-line long"></div>
                <div class="shimmer-line short"></div>
            </div>`;
        outputStatus.className   = 'output-status';
        outputStatus.textContent = '';
    }

    /**
     * Parse the plain-text output from friendlyCompiler.py / friendlyJavaCompiler.py
     * and render it as beautiful HTML cards.
     */
    function renderCompilerOutput(rawText, success) {
        welcomeScreen.style.display  = 'none';
        outputRendered.style.display = 'block';
        outputRendered.innerHTML     = '';

        // Update status pill
        if (success) {
            outputStatus.className   = 'output-status success';
            outputStatus.textContent = '✓ Compiled';
        } else {
            outputStatus.className   = 'output-status error';
            outputStatus.textContent = '✗ Failed';
        }

        if (!rawText || !rawText.trim()) {
            appendBlock('plain', 'No Output', 'The compiler produced no output.');
            return;
        }

        const lines = rawText.split('\n');

        if (success) {
            // ── Success path ──
            // Look for [SUCCESS] header and [Program Output] section
            let programOutputLines = [];
            let inProgramOutput    = false;
            let patternLine        = '';

            for (const line of lines) {
                if (line.includes('[SUCCESS]')) {
                    appendBlock('success', '✓ Compilation Successful', 'Your code compiled without errors! Great job.');
                } else if (line.startsWith('[+] Loaded')) {
                    patternLine = line.trim();
                } else if (line.includes('[Program Output]')) {
                    inProgramOutput = true;
                } else if (inProgramOutput) {
                    programOutputLines.push(line);
                }
            }

            if (patternLine) {
                appendBlock('info', 'Pattern Engine', patternLine.replace('[+] ', ''));
            }

            if (programOutputLines.length > 0) {
                const progOut = programOutputLines.join('\n').trim();
                if (progOut) {
                    appendBlock('plain', '▶ Program Output', progOut);
                }
            }

        } else {
            // ── Failure path ──
            // Split into sections by the ======= dividers
            const sections = splitIntoSections(lines);

            let patternLine  = '';
            let foundSection = '';

            for (const section of sections) {
                const text = section.join('\n').trim();
                if (!text) continue;

                // Header section (FRIENDLY JAVA COMPILER / FRIENDLY C COMPILER)
                if (text.match(/FRIENDLY (C|JAVA) COMPILER/)) {
                    // skip — the badge already shows language
                    continue;
                }

                // Pattern loaded line
                if (text.startsWith('[+] Loaded')) {
                    patternLine = text;
                    continue;
                }

                // [FAILED] block
                if (text.includes('[FAILED]')) {
                    appendBlock('error', '✗ Compilation Failed',
                        'There are errors in your code. See explanations below.');
                    continue;
                }

                // [Found N issue(s)] line
                if (text.startsWith('[Found')) {
                    foundSection = text;
                    appendBlock('warning', '📋 Issues Found', text.replace('[Found', '').replace(']', '').trim() + ' issue(s) were found in your code.');
                    continue;
                }

                // Individual error block: ERROR #N | Line X | ERROR
                if (text.startsWith('ERROR #')) {
                    renderErrorCard(section);
                    continue;
                }

                // ERROR STATISTICS block
                if (text.includes('[ERROR STATISTICS]')) {
                    appendBlock('info', '📊 Statistics', text.replace('[ERROR STATISTICS]', '').trim());
                    continue;
                }

                // Fallback: show as plain
                if (text.trim() && !text.match(/^=+$/)) {
                    appendBlock('plain', '', text);
                }
            }

            if (patternLine) {
                appendBlock('info', '🔎 Pattern Engine', patternLine.replace('[+] ', ''));
            }
        }
    }

    /**
     * Split raw lines into sections separated by ======= lines.
     */
    function splitIntoSections(lines) {
        const sections = [];
        let current    = [];

        for (const line of lines) {
            if (/^={40,}/.test(line.trim())) {
                if (current.length) {
                    sections.push(current);
                    current = [];
                }
            } else {
                current.push(line);
            }
        }
        if (current.length) sections.push(current);
        return sections;
    }

    /**
     * Render one error card from its lines.
     * Expected structure:
     *   ERROR #N | Line X, Column Y | ERROR
     *   (blank)
     *   [What went wrong]
     *     explanation text...
     *   (blank)
     *   [Confidence] ##### 75%
     *   (blank)
     *   [Original compiler message]
     *     raw message
     */
    function renderErrorCard(lines) {
        const fullText = lines.join('\n');

        // Parse header
        const headerLine = lines[0] || '';
        const lineMatch  = headerLine.match(/Line (\d+)/);
        const lineNum    = lineMatch ? lineMatch[1] : '?';
        const isSeverity = headerLine.includes('ERROR') ? 'error' : 'warning';

        // Extract explanation
        let explanation    = '';
        let originalMsg    = '';
        let confidence     = 0;
        let inExplanation  = false;
        let inOriginal     = false;

        for (let i = 1; i < lines.length; i++) {
            const l = lines[i];
            const trimmed = l.trim();

            if (trimmed === '[What went wrong]') {
                inExplanation = true; inOriginal = false; continue;
            }
            if (trimmed === '[Original compiler message]') {
                inOriginal = true; inExplanation = false; continue;
            }
            if (trimmed.startsWith('[Confidence]')) {
                const pct = trimmed.match(/(\d+)%/);
                if (pct) confidence = parseInt(pct[1]);
                inExplanation = false; inOriginal = false; continue;
            }
            if (trimmed.startsWith('[!]') || trimmed.startsWith('[DEBUG]') || trimmed === '') {
                inExplanation = false; inOriginal = false;
            }

            if (inExplanation && trimmed) {
                explanation += (explanation ? '\n' : '') + trimmed;
            }
            if (inOriginal && trimmed) {
                originalMsg += (originalMsg ? '\n' : '') + trimmed;
            }
        }

        // Build card HTML
        const block = document.createElement('div');
        block.className = `out-block ${isSeverity === 'error' ? 'error' : 'warning'}`;

        const titleEl = document.createElement('div');
        titleEl.className   = 'out-block-title';
        titleEl.textContent = `${isSeverity === 'error' ? '❌' : '⚠️'}  Error on Line ${lineNum}`;
        block.appendChild(titleEl);

        if (explanation) {
            const bodyEl = document.createElement('div');
            bodyEl.className   = 'out-block-body';
            bodyEl.textContent = explanation;
            block.appendChild(bodyEl);
        } else {
            // Could not match pattern
            const bodyEl = document.createElement('div');
            bodyEl.className   = 'out-block-body';
            bodyEl.textContent = "I don't recognise this error yet — see the original message below.";
            block.appendChild(bodyEl);
        }

        if (originalMsg) {
            const sep = document.createElement('div');
            sep.style.cssText = 'margin-top:8px;font-size:11.5px;opacity:0.7;font-family:var(--font-ui);font-weight:600;';
            sep.textContent = 'Original compiler message:';
            block.appendChild(sep);

            const orig = document.createElement('div');
            orig.style.cssText = 'font-family:var(--font-mono);font-size:11.5px;opacity:0.8;margin-top:3px;';
            orig.textContent = originalMsg;
            block.appendChild(orig);
        }

        if (confidence > 0) {
            const barWrap = document.createElement('div');
            barWrap.className = 'confidence-bar-wrap';
            barWrap.innerHTML = `
                <span>Confidence</span>
                <div class="confidence-bar-track">
                    <div class="confidence-bar-fill" style="width:${confidence}%"></div>
                </div>
                <span>${confidence}%</span>
            `;
            block.appendChild(barWrap);
        }

        outputRendered.appendChild(block);
    }

    function appendBlock(type, title, body) {
        const block = document.createElement('div');
        block.className = `out-block ${type}`;

        if (title) {
            const titleEl = document.createElement('div');
            titleEl.className   = 'out-block-title';
            titleEl.textContent = title;
            block.appendChild(titleEl);
        }

        if (body) {
            const bodyEl = document.createElement('div');
            bodyEl.className   = 'out-block-body';
            bodyEl.textContent = body;
            block.appendChild(bodyEl);
        }

        outputRendered.appendChild(block);
    }

    function showOutput(blocks, success) {
        welcomeScreen.style.display  = 'none';
        outputRendered.style.display = 'block';
        outputRendered.innerHTML     = '';

        outputStatus.className   = `output-status ${success ? 'success' : 'error'}`;
        outputStatus.textContent = success ? '✓ Compiled' : '✗ Failed';

        blocks.forEach(b => appendBlock(b.type, b.title, b.body));
    }

    function renderTips(lang) {
        tipsList.innerHTML = '';
        tipsData[lang].forEach(tip => {
            const li = document.createElement('li');
            li.innerHTML = tip;
            tipsList.appendChild(li);
        });
    }

    // Set initial state
    showWelcome();

});
