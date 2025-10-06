// Optional: Add dashboard-specific functionality
document.addEventListener('DOMContentLoaded', function() {
    loadUserStats();
});

async function loadUserStats() {
    try {
        const response = await fetch('/api/user/stats');
        const stats = await response.json();
        console.log('User stats:', stats);
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}
