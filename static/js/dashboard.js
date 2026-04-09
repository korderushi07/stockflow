document.addEventListener('DOMContentLoaded', () => {

    // Helper formatting functions
    const currencyFormatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0
    });

    const chartDefaults = {
        color: '#94a3b8',
        plugins: { legend: { display: false } },
        scales: {
            x: { 
                ticks: { display: false }, 
                grid: { display: false, drawBorder: false } 
            },
            y: { 
                ticks: { color: '#cbd5e1', font: { size: 10 } }, 
                grid: { color: '#f8fafc', drawBorder: false },
                beginAtZero: true
            }
        }
    };

    // 1. STATS: Total Revenue, Total Products, etc.
    async function loadDashboardStats() {
        try {
            const response = await fetch('/api/stats');
            const data = await response.json();
            
            if(document.getElementById('total-products')) document.getElementById('total-products').innerText = data.total_products;
            if(document.getElementById('total-sales')) document.getElementById('total-sales').innerText = data.total_sales;
            if(document.getElementById('total-revenue')) document.getElementById('total-revenue').innerText = "₹" + data.total_revenue.toLocaleString();
            if(document.getElementById('active-alerts')) document.getElementById('active-alerts').innerText = data.active_alerts;
            
            // Materio custom widget
            if(document.getElementById('revenue-overview')) {
                document.getElementById('revenue-overview').innerText = "₹" + data.total_revenue.toLocaleString();
            }

        } catch (error) {
            console.error("Error fetching stats:", error);
        }
    }

    // 2. PRODUCTS: Top Stock Levels Chart & Materials In Stock Health
    async function loadProductsAndCharts() {
        try {
            const data = await fetch('/api/products').then(r => r.json());
            
            // Calculate Stock Health
            const totalProducts = data.length;
            const lowStockCount = data.filter(p => p.stock_qty < p.reorder_level).length;
            
            if (totalProducts > 0) {
                const healthPercentage = Math.round(((totalProducts - lowStockCount) / totalProducts) * 100);
                
                const percentText = document.getElementById('stock-health-text');
                const progressBar = document.getElementById('materials-progress');
                
                if (percentText) percentText.innerText = Math.max(0, healthPercentage) + "%";
                if (progressBar) {
                    setTimeout(() => {
                        progressBar.style.width = Math.max(0, healthPercentage) + "%";
                        // Change color if lower than 50%
                        if (healthPercentage < 50) progressBar.classList.replace('bg-materio', 'bg-gray-800');
                    }, 300);
                }
            }
            
            // Build Stock Levels Chart (Top 8 items)
            const ctx = document.getElementById('stockChart');
            if (ctx) {
                // sort by stock asc/desc? Or just take first 8.
                const topProducts = data.slice(0, 8);
                new Chart(ctx, {
                    type: "bar",
                    data: {
                        labels: topProducts.map(p => p.product.substring(0, 10) + '..'),
                        datasets: [{
                            label: "Stock Qty",
                            data: topProducts.map(p => p.stock_qty),
                            backgroundColor: "#1E293B",
                            hoverBackgroundColor: "#FFB547",
                            borderRadius: 6,
                            barPercentage: 0.8,
                            categoryPercentage: 0.7
                        }]
                    },
                    options: {
                        ...chartDefaults,
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: { legend: { display: false }, tooltip: { cornerRadius: 8, padding: 10 } }
                    }
                });
            }

        } catch(error) {
            console.error("Error fetching products:", error);
        }
    }

    // 3. SALES: Revenue Doughnut Chart
    async function loadSalesAndRevenue() {
        try {
            const data = await fetch('/api/sales').then(r => r.json());
            
            const grouped = {};
            data.forEach(s => {
                grouped[s.product] = (grouped[s.product] || 0) + parseFloat(s.total_amount);
            });

            const ctx = document.getElementById("revenueChart");
            if (ctx) {
                new Chart(ctx, {
                    type: "doughnut",
                    data: {
                        labels: Object.keys(grouped).map(k => k.substring(0, 15)),
                        datasets: [{
                            data: Object.values(grouped),
                            backgroundColor: ["#0F172A", "#1E293B", "#334155", "#475569", "#64748B", "#94A3B8", "#CBD5E1"],
                            borderWidth: 2,
                            borderColor: '#ffffff',
                            hoverOffset: 4
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { display: false },
                            tooltip: { cornerRadius: 8, padding: 10 }
                        },
                        cutout: "75%"
                    }
                });
            }

        } catch (error) {
             console.error("Error fetching sales:", error);
        }
    }

    // 4. ALERTS: Recent Activity Feed
    async function loadRecentAlerts() {
        try {
            const data = await fetch("/api/alerts").then(r => r.json());
            const listEl = document.getElementById("recent-alerts-list");
            
            if (!listEl) return;
            
            if (data.length === 0) {
                listEl.innerHTML = '<li class="text-center text-gray-400 py-4">No recent alerts found.</li>';
                return;
            }
            
            // Show only the 5 most recent
            const recent = data.slice(0, 5);
            
            listEl.innerHTML = recent.map(a => {
                const iconClass = a.is_resolved 
                    ? 'bg-gray-100 text-gray-400' 
                    : 'bg-gray-800 text-white shadow-sm';
                
                const iconLucide = a.is_resolved ? 'check' : 'alert-circle';
                
                // Clean up emojis and parse the raw | separated data
                let cleanMsg = a.alert_message.replace(/⚠️\s*/g, '');
                let formattedMsg = `<p class="text-xs text-gray-500 mt-1 line-clamp-2">${cleanMsg}</p>`;
                
                if (cleanMsg.includes('|')) {
                    const parts = cleanMsg.split('|').map(p => p.trim());
                    // parts[1] is e.g. "Current: 7", parts[2] is "Reorder Level: 10"
                    const currentQty = parts[1] ? parts[1].split(':')[1]?.trim() : '?';
                    const targetQty = parts[2] ? parts[2].split(':')[1]?.trim() : '?';
                    
                    formattedMsg = `
                        <div class="flex items-center space-x-2 mt-2">
                            <span class="bg-gray-50 text-gray-900 px-2 py-0.5 rounded text-[11px] border border-gray-200 font-medium tracking-wide">STOCK: <span class="text-red-500 ml-1">${currentQty}</span></span>
                            <span class="bg-gray-50 text-gray-500 px-2 py-0.5 rounded text-[11px] border border-gray-200 tracking-wide">MIN: <span class="font-medium">${targetQty}</span></span>
                        </div>
                    `;
                }
                
                return `
                <li class="flex items-start">
                    <div class="flex-shrink-0 mt-1">
                        <div class="w-8 h-8 rounded-full flex items-center justify-center ${iconClass}">
                            <i data-lucide="${iconLucide}" class="w-4 h-4"></i>
                        </div>
                    </div>
                    <div class="ml-4 flex-1">
                        <div class="flex items-center justify-between">
                            <span class="text-sm font-semibold text-gray-800">${a.product}</span>
                            <span class="text-[11px] text-gray-400 font-medium">${a.alert_time.split(' ')[0]}</span>
                        </div>
                        ${formattedMsg}
                    </div>
                </li>
                `;
            }).join("");
            
            if(window.lucide) {
                lucide.createIcons();
            }

        } catch (error) {
            console.error("Error fetching alerts:", error);
        }
    }

    // Run setup
    // 5. SIDEBAR FLOATING ICONS LOGIC
    const btnCalendar = document.getElementById('btn-calendar');
    const btnChart = document.getElementById('btn-chart');
    const btnTruck = document.getElementById('btn-truck');
    const btnUsers = document.getElementById('btn-users');
    const btnAlert = document.getElementById('btn-alert');

    // Chart: scroll to canvas
    if (btnChart) {
        btnChart.addEventListener('click', (e) => {
            e.preventDefault();
            document.getElementById('stockChart')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
        });
    }

    // Alert: scroll to alerts list
    if (btnAlert) {
        btnAlert.addEventListener('click', (e) => {
            e.preventDefault();
            document.getElementById('recent-alerts-list')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
        });
    }

    // Calendar: trigger toast
    if (btnCalendar) {
        btnCalendar.addEventListener('click', (e) => {
            e.preventDefault();
            const now = new Date();
            const dateStr = now.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' });
            showToast(`System synced: ${dateStr}`);
        });
    }

    // Truck: Load Suppliers Modal
    if (btnTruck) {
        btnTruck.addEventListener('click', async (e) => {
            e.preventDefault();
            try {
                const data = await fetch('/api/suppliers').then(r => r.json());
                const list = document.getElementById('suppliers-list');
                if(data.length === 0) list.innerHTML = `<li class="text-center text-sm text-gray-400 py-4">No active suppliers found.</li>`;
                else {
                    list.innerHTML = data.map(s => `
                        <li class="bg-gray-50 border border-gray-100 rounded-lg p-4 flex items-center justify-between">
                            <div>
                                <h4 class="font-bold text-gray-800 text-sm">${s.name}</h4>
                                <p class="text-xs text-gray-500 flex items-center mt-1"><i data-lucide="phone" class="w-3 h-3 mr-1"></i> ${s.phone || 'N/A'}</p>
                            </div>
                            <span class="text-[10px] font-bold bg-green-100 text-green-700 px-2 py-0.5 rounded uppercase tracking-wider">Active</span>
                        </li>
                    `).join('');
                    if(window.lucide) lucide.createIcons();
                }
                openModal('suppliers-modal');
            } catch (err) {
                console.error("Error fetching suppliers:", err);
            }
        });
    }

    // Users: Load Customers Modal
    if (btnUsers) {
        btnUsers.addEventListener('click', async (e) => {
            e.preventDefault();
            try {
                const data = await fetch('/api/customers').then(r => r.json());
                const list = document.getElementById('customers-list');
                if(data.length === 0) list.innerHTML = `<li class="text-center text-sm text-gray-400 py-4">No customers found.</li>`;
                else {
                    list.innerHTML = data.map(c => `
                        <li class="bg-gray-50 border border-gray-100 rounded-lg p-4 flex items-center justify-between">
                            <div>
                                <h4 class="font-bold text-gray-800 text-sm">${c.full_name}</h4>
                                <p class="text-xs text-gray-500 mt-1 flex items-center"><i data-lucide="mail" class="w-3 h-3 mr-1"></i> ${c.email || 'N/A'}</p>
                            </div>
                        </li>
                    `).join('');
                    if(window.lucide) lucide.createIcons();
                }
                openModal('customers-modal');
            } catch (err) {
                console.error("Error fetching customers:", err);
            }
        });
    }

    // Helper functions for UI
    function openModal(modalId) {
        const overlay = document.getElementById('modal-overlay');
        const modal = document.getElementById(modalId);
        
        if(!overlay || !modal) return;

        overlay.classList.remove('hidden');
        modal.classList.remove('hidden');
        
        setTimeout(() => {
            modal.classList.add('opacity-100', 'scale-100');
        }, 10);
    }
    
    function showToast(msg) {
        const toast = document.getElementById('toast-notify');
        if(!toast) return;
        document.getElementById('toast-text').innerText = msg;
        toast.classList.remove('hidden');
        setTimeout(() => toast.classList.remove('translate-y-10'), 10);
        setTimeout(() => {
            toast.classList.add('translate-y-10');
            setTimeout(() => toast.classList.add('hidden'), 300);
        }, 3000);
    }

    // Run setup
    loadDashboardStats();
    loadProductsAndCharts();
    loadSalesAndRevenue();
    loadRecentAlerts();

});
