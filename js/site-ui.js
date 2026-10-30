/**
 * Akkireddy Challa - Modern Agentic Portfolio UI
 * High-performance, dependency-free vanilla JavaScript
 * Follows modern-web-guidance best practices
 */

(() => {
    'use strict';

    // =========================================================================
    // 1. Theme Management (System, Dark, Light)
    // =========================================================================
    const root = document.documentElement;
    const themeMeta = document.querySelector('meta[name="color-scheme"]');
    const themeToggle = document.getElementById('theme-toggle');

    const getSavedTheme = () => {
        try {
            return localStorage.getItem('site-theme');
        } catch {
            return null;
        }
    };

    const applyTheme = (theme, persist = false) => {
        if (!theme) {
            // Default to system
            const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            theme = systemPrefersDark ? 'dark' : 'light';
        }

        root.dataset.theme = theme;
        if (themeMeta) {
            themeMeta.content = theme;
        }

        if (persist) {
            try {
                localStorage.setItem('site-theme', theme);
            } catch (e) {}
        }

        updateThemeIcon(theme);
    };

    const updateThemeIcon = (theme) => {
        if (!themeToggle) return;
        const isDark = theme === 'dark';
        themeToggle.innerHTML = isDark
            ? `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>`
            : `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>`;
        themeToggle.setAttribute('aria-label', isDark ? 'Switch to light mode' : 'Switch to dark mode');
    };

    // Initialize Theme
    const savedTheme = getSavedTheme();
    applyTheme(savedTheme, false);

    themeToggle?.addEventListener('click', () => {
        const currentTheme = root.dataset.theme === 'dark' ? 'dark' : 'light';
        const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
        applyTheme(nextTheme, true);
        showToast(`Theme switched to ${nextTheme} mode`);
    });

    // Sync across browser tabs
    window.addEventListener('storage', (e) => {
        if (e.key === 'site-theme' && (e.newValue === 'dark' || e.newValue === 'light')) {
            applyTheme(e.newValue, false);
        }
    });

    // Listen to OS system preference change if user hasn't explicitly set a preference
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (!getSavedTheme()) {
            applyTheme(e.matches ? 'dark' : 'light', false);
        }
    });

    // =========================================================================
    // 2. Header Scroll & Reading Progress
    // =========================================================================
    const siteHeader = document.querySelector('.site-header');
    const readingProgress = document.querySelector('[data-reading-progress]');

    const onScroll = () => {
        const scrollY = window.scrollY;

        // Header glassmorphic elevation
        if (siteHeader) {
            if (scrollY > 40) {
                siteHeader.classList.add('scrolled');
            } else {
                siteHeader.classList.remove('scrolled');
            }
        }

        // Reading progress indicator
        if (readingProgress) {
            const docHeight = document.documentElement.scrollHeight - window.innerHeight;
            const progress = docHeight > 0 ? Math.min(1, Math.max(0, scrollY / docHeight)) : 0;
            readingProgress.style.setProperty('--reading-progress', progress);
        }
    };

    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    // =========================================================================
    // 3. Stockholm Real-Time Clock & Telemetry
    // =========================================================================
    const stockholmClockElem = document.getElementById('stockholm-clock');

    const updateStockholmTime = () => {
        if (!stockholmClockElem) return;
        try {
            const now = new Date();
            const timeString = new Intl.DateTimeFormat('en-GB', {
                timeZone: 'Europe/Stockholm',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                hour12: false
            }).format(now);
            stockholmClockElem.textContent = `${timeString} CET`;
        } catch (e) {
            stockholmClockElem.textContent = 'Stockholm UTC+1';
        }
    };

    updateStockholmTime();
    setInterval(updateStockholmTime, 1000);

    // =========================================================================
    // 4. Interactive MCP Agent Studio Playground
    // =========================================================================
    const mcpData = {
        'k8s-mcp': {
            title: 'k8s-mcp-server',
            repo: 'https://github.com/akkireddy-challa/k8s-mcp-server',
            command: 'agent.call_tool("k8s_diagnose_pod", { namespace: "prod", pod: "auth-api-89fd" })',
            output: `[MCP: k8s-mcp-server v0.4.1 connected via stdio]
→ Querying Kubernetes API: pods in namespace 'prod'
✓ Found Pod: auth-api-89fd (Container: core-auth)
⚠ Status: CrashLoopBackOff (Restart Count: 5)
▶ Root Cause Identified: OOMKilled (Exit Code: 137)
  Memory Peak: 512Mi | Limit: 512Mi
💡 AI Remediation Hint:
  - Increase container limits to 768Mi in Helm values.yaml
  - Patch ready: deployment/auth-api • namespace/prod`,
            configSnippet: `{
  "mcpServers": {
    "k8s-mcp": {
      "command": "python3",
      "args": ["-m", "k8s_mcp_server"],
      "env": { "KUBECONFIG": "~/.kube/config" }
    }
  }
}`
        },
        'azure-mcp': {
            title: 'azure-mcp-platform',
            repo: 'https://github.com/akkireddy-challa/azure-mcp-platform',
            command: 'agent.call_tool("azure_inspect_ai_foundry", { resource_group: "rg-sweden-ai" })',
            output: `[MCP: azure-mcp-platform v0.3.0 connected via Entra ID ADC]
→ Authenticating via Managed Identity (DefaultAzureCredential)
✓ Azure Subscription: Sweden Central Production
✓ Connected to Azure AI Foundry Hub: 'sweden-north-ai-hub'
Model Endpoints Deployed:
  1. gpt-4o (GlobalStandard) • TPM: 450,000 • Status: Healthy (P95: 380ms)
  2. deepseek-r1 (Dedicated H100) • TPM: 200,000 • Status: Ready
🔒 Compliance: Private Endpoint Enabled • Zero Hardcoded Secrets`,
            configSnippet: `{
  "mcpServers": {
    "azure-mcp": {
      "command": "python3",
      "args": ["-m", "azure_mcp_platform"],
      "env": { "AZURE_TENANT_ID": "default" }
    }
  }
}`
        },
        'grafana-mcp': {
            title: 'grafana-mcp-observability',
            repo: 'https://github.com/akkireddy-challa/grafana-mcp-observability',
            command: 'agent.call_tool("grafana_query_slo_alerts", { service: "gke-ingress-gateway" })',
            output: `[MCP: grafana-mcp-observability v0.2.8]
→ Connecting to Prometheus Datasource & Loki Log Stream
✓ Target: gke-ingress-gateway (Cluster: gke-eu-north1)
SLO Metrics (Window: Last 1 hour):
  - Availability SLO Target: 99.90% | Current: 99.98% (Pass)
  - Latency P99: 44.8ms (Target < 120ms)
  - Active PromQL Alerts: 0 firing, 0 pending
  - Error Budget Burn Rate: 0.12x (Extremely Healthy)`,
            configSnippet: `{
  "mcpServers": {
    "grafana-mcp": {
      "command": "python3",
      "args": ["-m", "grafana_mcp_observability"],
      "env": { "GRAFANA_URL": "https://grafana.internal" }
    }
  }
}`
        },
        'phoenix-mcp': {
            title: 'phoenix-mcp-eval',
            repo: 'https://github.com/akkireddy-challa/phoenix-mcp-eval',
            command: 'agent.call_tool("phoenix_trace_eval", { project: "nova-researcher", sample: 25 })',
            output: `[MCP: phoenix-mcp-eval v0.1.5]
→ Arize Phoenix OpenTelemetry Collector connected (Port 6006)
Trace Benchmark Evaluation Results:
  - Total AI Agent Turns Analyzed: 25
  - Citation Precision Score: 99.2%
  - Hallucination Rate: 0.00% (Passed safety threshold)
  - Tool Calling Success Rate: 100%
  - Average End-to-End Latency: 512ms
Verdict: Ready for production agent deployment.`,
            configSnippet: `{
  "mcpServers": {
    "phoenix-mcp": {
      "command": "python3",
      "args": ["-m", "phoenix_mcp_eval"],
      "env": { "PHOENIX_COLLECTOR_ENDPOINT": "http://localhost:6006" }
    }
  }
}`
        }
    };

    let activeMcpKey = 'k8s-mcp';

    const mcpTabs = document.querySelectorAll('.mcp-tab');
    const terminalCmdText = document.getElementById('terminal-cmd-text');
    const terminalOutput = document.getElementById('terminal-output');
    const mcpRepoLink = document.getElementById('mcp-repo-link');
    const btnRunTool = document.getElementById('btn-run-tool');
    const btnCopyConfig = document.getElementById('btn-copy-config');

    const updateMcpStudio = (key) => {
        activeMcpKey = key;
        const data = mcpData[key];
        if (!data) return;

        mcpTabs.forEach(tab => {
            const isActive = tab.dataset.mcp === key;
            tab.classList.toggle('active', isActive);
            tab.setAttribute('aria-selected', isActive ? 'true' : 'false');
            tab.tabIndex = isActive ? 0 : -1;
        });

        if (terminalCmdText) terminalCmdText.textContent = data.command;
        if (terminalOutput) {
            terminalOutput.classList.remove('is-running');
            terminalOutput.textContent = data.output;
            terminalOutput.parentElement.scrollTop = 0;
        }
        if (mcpRepoLink) {
            mcpRepoLink.href = data.repo;
            mcpRepoLink.textContent = `Open ${data.title} ↗`;
        }
    };

    mcpTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const key = tab.dataset.mcp;
            if (key) updateMcpStudio(key);
        });
        tab.addEventListener('keydown', (event) => {
            const currentIndex = Array.from(mcpTabs).indexOf(tab);
            let nextIndex = null;
            if (event.key === 'ArrowRight') nextIndex = (currentIndex + 1) % mcpTabs.length;
            if (event.key === 'ArrowLeft') nextIndex = (currentIndex - 1 + mcpTabs.length) % mcpTabs.length;
            if (event.key === 'Home') nextIndex = 0;
            if (event.key === 'End') nextIndex = mcpTabs.length - 1;
            if (nextIndex === null) return;
            event.preventDefault();
            const nextTab = mcpTabs[nextIndex];
            updateMcpStudio(nextTab.dataset.mcp);
            nextTab.focus();
        });
    });

    btnRunTool?.addEventListener('click', () => {
        const data = mcpData[activeMcpKey];
        if (!data || !terminalOutput) return;

        terminalOutput.textContent = '⏳ Executing agent tool in isolated sandbox...';
        terminalOutput.classList.add('is-running');
        btnRunTool.disabled = true;

        setTimeout(() => {
            terminalOutput.textContent = data.output;
            terminalOutput.classList.remove('is-running');
            terminalOutput.parentElement.scrollTop = 0;
            btnRunTool.disabled = false;
            showToast(`✓ Tool executed successfully`);
        }, 350);
    });

    btnCopyConfig?.addEventListener('click', () => {
        const data = mcpData[activeMcpKey];
        if (!data) return;

        navigator.clipboard.writeText(data.configSnippet).then(() => {
            showToast(`MCP config for ${data.title} copied!`);
        }).catch(() => {
            showToast('Unable to copy to clipboard');
        });
    });

    // =========================================================================
    // 5. Bento Grid Category Filter
    // =========================================================================
    const filterPills = document.querySelectorAll('.filter-pill');
    const bentoCards = document.querySelectorAll('.bento-card');

    filterPills.forEach(pill => {
        pill.addEventListener('click', () => {
            const filter = pill.dataset.filter;

            filterPills.forEach(p => {
                const isActive = p === pill;
                p.classList.toggle('active', isActive);
                p.setAttribute('aria-pressed', isActive ? 'true' : 'false');
            });

            bentoCards.forEach(card => {
                const category = card.dataset.category || '';
                const tags = card.dataset.tags || '';
                const matches = filter === 'all' || category.includes(filter) || tags.includes(filter);

                if (matches) {
                    card.style.display = 'flex';
                    card.style.animation = 'fadeInCard 0.25s ease forwards';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });

    // Keep the floating navigation in sync with the section currently in view.
    const navLinks = document.querySelectorAll('.nav-link[href^="#"]');
    const navSections = Array.from(navLinks)
        .map(link => document.querySelector(link.getAttribute('href')))
        .filter(Boolean);

    if ('IntersectionObserver' in window && navSections.length) {
        const sectionObserver = new IntersectionObserver((entries) => {
            const visibleSection = entries
                .filter(entry => entry.isIntersecting)
                .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
            if (!visibleSection) return;
            navLinks.forEach(link => {
                link.classList.toggle('active', link.getAttribute('href') === `#${visibleSection.target.id}`);
            });
        }, { rootMargin: '-28% 0px -58% 0px', threshold: [0.1, 0.35, 0.6] });

        navSections.forEach(section => sectionObserver.observe(section));
    }

    // =========================================================================
    // 6. Fast Email Copy Buttons & Toast Notifications
    // =========================================================================
    const emailToCopy = 'challaakkireddy@gmail.com';
    const copyEmailButtons = document.querySelectorAll('[data-copy-email]');

    copyEmailButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            navigator.clipboard.writeText(emailToCopy).then(() => {
                showToast(`Copied ${emailToCopy} to clipboard!`);
            }).catch(() => {
                window.location.href = `mailto:${emailToCopy}`;
            });
        });
    });

    const toastContainer = document.getElementById('toast-container');
    let toastTimeout = null;

    window.showToast = (message) => {
        if (!toastContainer) return;

        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> <span>${message}</span>`;

        toastContainer.appendChild(toast);

        // Trigger reflow to animate
        requestAnimationFrame(() => {
            toast.classList.add('show');
        });

        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 250);
        }, 3000);
    };

    // =========================================================================
    // 7. Command Palette (Cmd + K / Ctrl + K)
    // =========================================================================
    const cmdDialog = document.getElementById('cmd-dialog');
    const cmdInput = document.getElementById('cmd-input');
    const cmdResults = document.getElementById('cmd-results');
    const cmdTriggers = document.querySelectorAll('[data-open-cmd]');

    const cmdItems = [
        { title: 'K8s MCP Server', category: 'MCP Tool', desc: 'Kubernetes diagnostic and debugging agent tool', url: 'https://github.com/akkireddy-challa/k8s-mcp-server', external: true },
        { title: 'Azure MCP Platform', category: 'MCP Tool', desc: 'Azure AI Foundry and Entra ID management tool', url: 'https://github.com/akkireddy-challa/azure-mcp-platform', external: true },
        { title: 'Grafana MCP Observability', category: 'MCP Tool', desc: 'Query Grafana alerts and metrics from agents', url: 'https://github.com/akkireddy-challa/grafana-mcp-observability', external: true },
        { title: 'Phoenix MCP Eval', category: 'MCP Tool', desc: 'LLM tracing and hallucination benchmark eval', url: 'https://github.com/akkireddy-challa/phoenix-mcp-eval', external: true },
        { title: 'Nova: Autonomous AI Researcher', category: 'Project', desc: 'Self-hosted research assistant with cited cards & multi-LLMs', url: 'https://github.com/akkireddy-challa/nova', external: true },
        { title: 'PitchRoast: AI Venture Committee', category: 'Hackathon', desc: 'Stockholm Claude Hackathon startup roaster', url: 'https://github.com/akkireddy-challa/pitchroast', external: true },
        { title: 'Bounce 3D (WebGPU Game Jam)', category: 'GameTech', desc: 'Stockholm AWS & Bitmagic Game Jam entry', url: 'https://github.com/akkireddy-challa/bounce-3d', external: true },
        { title: 'AWS Analytics Platform Terraform', category: 'Terraform', desc: 'Production multi-cloud data infrastructure IaC', url: 'https://github.com/akkireddy-challa/aws-analytics-platform-terraform', external: true },
        { title: 'Cloud Platform Operating Model', category: 'Writing', desc: 'Article: Shared operating model for reliability & cost', url: 'writing/cloud-platform-operating-model.html', external: false },
        { title: 'Practical AI Infrastructure Foundations', category: 'Writing', desc: 'Article: Scalable compute, artifact paths & FinOps for AI', url: 'writing/ai-infrastructure-foundations.html', external: false },
        { title: 'Terraform Best Practices', category: 'Writing', desc: 'Article: State discipline, small modules & safe plans', url: 'writing/terraform-best-practices.html', external: false },
        { title: 'Download Resume (CV)', category: 'Download', desc: 'PDF: Akkireddy Challa Platform Engineer CV', url: 'images/AkkireddyCV19.pdf', external: true },
        { title: 'Toggle Light / Dark Theme', category: 'Action', action: 'toggle-theme', desc: 'Switch site color mode' },
        { title: 'Copy Email Address', category: 'Action', action: 'copy-email', desc: 'challaakkireddy@gmail.com' }
    ];

    const openCmdPalette = () => {
        if (!cmdDialog) return;
        cmdDialog.showModal();
        if (cmdInput) {
            cmdInput.value = '';
            cmdInput.focus();
        }
        renderCmdResults('');
    };

    const closeCmdPalette = () => {
        if (!cmdDialog) return;
        cmdDialog.close();
    };

    cmdTriggers.forEach(btn => btn.addEventListener('click', openCmdPalette));

    document.addEventListener('keydown', (e) => {
        if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
            e.preventDefault();
            if (cmdDialog?.open) {
                closeCmdPalette();
            } else {
                openCmdPalette();
            }
        }
        if (e.key === 'Escape' && cmdDialog?.open) {
            closeCmdPalette();
        }
    });

    cmdDialog?.addEventListener('click', (e) => {
        if (e.target === cmdDialog) {
            closeCmdPalette();
        }
    });

    const renderCmdResults = (query) => {
        if (!cmdResults) return;
        const q = query.toLowerCase().trim();
        const filtered = cmdItems.filter(item =>
            item.title.toLowerCase().includes(q) ||
            item.category.toLowerCase().includes(q) ||
            (item.desc && item.desc.toLowerCase().includes(q))
        );

        if (filtered.length === 0) {
            cmdResults.innerHTML = `<div style="padding: 24px; text-align: center; color: var(--text-muted); font-size: 0.9rem;">No matching commands or projects found.</div>`;
            return;
        }

        cmdResults.innerHTML = filtered.map((item, index) => `
            <div class="cmd-item ${index === 0 ? 'selected' : ''}" data-index="${index}" role="option">
                <div class="cmd-item-left">
                    <span class="cmd-item-badge">${item.category}</span>
                    <div>
                        <div style="font-weight: 600; color: var(--text-primary);">${item.title}</div>
                        <div style="font-size: 0.76rem; color: var(--text-muted);">${item.desc}</div>
                    </div>
                </div>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
            </div>
        `).join('');

        // Item click listeners
        cmdResults.querySelectorAll('.cmd-item').forEach((elem, i) => {
            elem.addEventListener('click', () => {
                executeCmdItem(filtered[i]);
            });
        });
    };

    const executeCmdItem = (item) => {
        if (!item) return;
        closeCmdPalette();

        if (item.action === 'toggle-theme') {
            const nextTheme = root.dataset.theme === 'dark' ? 'light' : 'dark';
            applyTheme(nextTheme, true);
            showToast(`Theme switched to ${nextTheme} mode`);
        } else if (item.action === 'copy-email') {
            navigator.clipboard.writeText(emailToCopy).then(() => {
                showToast(`Copied ${emailToCopy}!`);
            });
        } else if (item.url) {
            if (item.external) {
                window.open(item.url, '_blank', 'noopener,noreferrer');
            } else {
                window.location.href = item.url;
            }
        }
    };

    cmdInput?.addEventListener('input', (e) => {
        renderCmdResults(e.target.value);
    });

    cmdInput?.addEventListener('keydown', (e) => {
        const items = cmdResults?.querySelectorAll('.cmd-item');
        if (!items || items.length === 0) return;

        let selectedIndex = Array.from(items).findIndex(el => el.classList.contains('selected'));

        if (e.key === 'ArrowDown') {
            e.preventDefault();
            selectedIndex = (selectedIndex + 1) % items.length;
            items.forEach((el, idx) => el.classList.toggle('selected', idx === selectedIndex));
            items[selectedIndex]?.scrollIntoView({ block: 'nearest' });
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            selectedIndex = (selectedIndex - 1 + items.length) % items.length;
            items.forEach((el, idx) => el.classList.toggle('selected', idx === selectedIndex));
            items[selectedIndex]?.scrollIntoView({ block: 'nearest' });
        } else if (e.key === 'Enter') {
            e.preventDefault();
            items[selectedIndex]?.click();
        }
    });

    // =========================================================================
    // 8. Mobile Navigation Drawer
    // =========================================================================
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');

    navToggle?.addEventListener('click', () => {
        const isOpen = navMenu?.classList.toggle('open');
        navToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });

    navMenu?.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('open');
            navToggle?.setAttribute('aria-expanded', 'false');
        });
    });

    // Close on outside click
    document.addEventListener('click', (e) => {
        if (navMenu?.classList.contains('open') && !navMenu.contains(e.target) && !navToggle?.contains(e.target)) {
            navMenu.classList.remove('open');
            navToggle?.setAttribute('aria-expanded', 'false');
        }
    });

})();
