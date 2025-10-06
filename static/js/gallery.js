// Gallery JavaScript functionality

class Gallery {
    constructor() {
        this.initializeElements();
        this.attachEventListeners();
        this.addAnimations();
    }

    initializeElements() {
        this.modal = document.getElementById('imageModal');
        this.modalImage = document.getElementById('modalImage');
        this.modalTitle = document.getElementById('modalTitle');
        this.modalDate = document.getElementById('modalDate');
        this.galleryItems = document.querySelectorAll('.gallery-item');
    }

    attachEventListeners() {
        // Close modal when clicking outside or on close button
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal || e.target.classList.contains('close')) {
                this.closeModal();
            }
        });

        // Close modal with Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.modal.style.display === 'flex') {
                this.closeModal();
            }
        });
    }

    addAnimations() {
        // Add stagger animation to gallery items
        this.galleryItems.forEach((item, index) => {
            item.style.opacity = '0';
            item.style.transform = 'translateY(30px)';
            item.style.animation = `fadeInUp 0.6s ease-out ${index * 0.1}s forwards`;
        });
    }

    openModal(imageUrl, filename, timestamp) {
        this.modalImage.src = imageUrl;
        this.modalTitle.textContent = filename;
        this.modalDate.textContent = timestamp;
        this.modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }

    closeModal() {
        this.modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }

    downloadModalImage() {
        const imageUrl = this.modalImage.src;
        const filename = this.modalTitle.textContent;
        downloadImage(imageUrl, filename);
    }

    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        const icon = this.getToastIcon(type);
        toast.innerHTML = `
            <i class="fas ${icon}"></i>
            <span>${message}</span>
        `;
        
        const container = document.getElementById('toast-container');
        container.appendChild(toast);
        
        // Trigger animation
        setTimeout(() => toast.classList.add('show'), 100);
        
        // Remove toast after 5 seconds
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => container.removeChild(toast), 300);
        }, 5000);
    }

    getToastIcon(type) {
        switch (type) {
            case 'success': return 'fa-check-circle';
            case 'error': return 'fa-exclamation-circle';
            case 'warning': return 'fa-exclamation-triangle';
            default: return 'fa-info-circle';
        }
    }
}

// Global functions
function openImageModal(imageUrl, filename, timestamp) {
    window.gallery.openModal(imageUrl, filename, timestamp);
}

function closeImageModal() {
    window.gallery.closeModal();
}

function downloadModalImage() {
    window.gallery.downloadModalImage();
}

function downloadImage(url, filename) {
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    // Show toast notification
    if (window.gallery) {
        window.gallery.showToast('Download started', 'success');
    }
}

// Initialize gallery when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.gallery = new Gallery();
});

// Add parallax effect to gallery header
document.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const parallax = document.querySelector('.gallery-header');
    if (parallax) {
        const speed = scrolled * 0.5;
        parallax.style.transform = `translateY(${speed}px)`;
    }
});

// Add hover effects for gallery items
document.addEventListener('DOMContentLoaded', () => {
    const galleryItems = document.querySelectorAll('.gallery-item');
    
    galleryItems.forEach(item => {
        item.addEventListener('mouseenter', () => {
            item.style.transform = 'translateY(-10px) scale(1.02)';
        });
        
        item.addEventListener('mouseleave', () => {
            item.style.transform = 'translateY(0) scale(1)';
        });
    });
});

// Add CSS animations for gallery
const galleryStyle = document.createElement('style');
galleryStyle.textContent = `
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes modalSlideIn {
        from {
            opacity: 0;
            transform: scale(0.8);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    .modal-content {
        animation: modalSlideIn 0.3s ease-out;
    }
    
    .gallery-item {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .image-overlay {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .view-btn, .download-btn {
        transform: translateY(10px);
        transition: all 0.3s ease;
    }
    
    .gallery-item:hover .view-btn,
    .gallery-item:hover .download-btn {
        transform: translateY(0);
    }
`;
document.head.appendChild(galleryStyle);

let currentImageUrl = '';
let currentFilename = '';

// Setup event listeners when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    setupGalleryListeners();
});

function setupGalleryListeners() {
    // Gallery item clicks
    document.querySelectorAll('.gallery-item').forEach(item => {
        item.addEventListener('click', function(e) {
            // Don't open modal if clicking download button
            if (e.target.closest('.download-btn')) {
                return;
            }
            
            const url = this.dataset.imageUrl;
            const filename = this.dataset.filename;
            const timestamp = this.dataset.timestamp;
            const prompt = this.dataset.prompt;
            
            openImageModal(url, filename, timestamp, prompt);
        });
    });
    
    // Download button clicks
    document.querySelectorAll('.download-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            const url = this.dataset.downloadUrl;
            const filename = this.dataset.downloadFilename;
            downloadImage(url, filename);
        });
    });
    
    // Close modal on backdrop click
    const modal = document.getElementById('imageModal');
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal || e.target.classList.contains('modal-backdrop')) {
                closeImageModal();
            }
        });
    }
}

function openImageModal(url, filename, timestamp, prompt) {
    const modal = document.getElementById('imageModal');
    const modalImage = document.getElementById('modalImage');
    const modalTitle = document.getElementById('modalTitle');
    const modalDate = document.getElementById('modalDate');
    const modalPrompt = document.getElementById('modalPrompt');
    
    if (!modal) {
        console.error('Modal element not found');
        return;
    }
    
    currentImageUrl = url;
    currentFilename = filename;
    
    modalImage.src = url;
    modalTitle.textContent = filename;
    modalDate.textContent = timestamp;
    if (modalPrompt) {
        modalPrompt.textContent = prompt || 'No prompt available';
    }
    
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden'; // Prevent background scrolling
}

function closeImageModal() {
    const modal = document.getElementById('imageModal');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = ''; // Restore scrolling
    }
}

function downloadImage(url, filename) {
    // Create a temporary link and trigger download
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.target = '_blank'; // Fallback for some browsers
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    
    // Show success message
    showToast('Download started!', 'success');
}

function downloadModalImage() {
    downloadImage(currentImageUrl, currentFilename);
}

// Close modal with Escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeImageModal();
    }
});

// Toast notification function
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container') || createToastContainer();
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        ${message}
    `;
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.classList.add('show');
    }, 10);
    
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container';
    document.body.appendChild(container);
    return container;
}
