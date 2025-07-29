document.addEventListener("DOMContentLoaded", function () {
    const confirmModal = document.getElementById("confirmModal");
    const confirmDeleteBtn = document.getElementById("confirmDeleteBtn");

    if (confirmModal && confirmDeleteBtn) {
        const modalInstance = new bootstrap.Modal(confirmModal);

        document.querySelectorAll(".btn-delete").forEach(button => {
            button.addEventListener("click", function () {
                const reminderId = this.dataset.id;
                confirmDeleteBtn.dataset.id = reminderId;
                modalInstance.show();
            });
        });

        confirmDeleteBtn.addEventListener("click", function () {
            const id = this.dataset.id;
            window.location.href = `/delete/${id}`;
        });
    }

    // SEARCH logic
    const searchInput = document.getElementById('search');
    if (searchInput) {
        searchInput.addEventListener('input', function () {
            const query = this.value;
            fetch(`/search?q=${encodeURIComponent(query)}`)
                .then(response => response.text())
                .then(html => {
                    document.getElementById('reminder-table').innerHTML = html;
                });
        });
    }
});
