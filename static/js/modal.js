 // 1. Selecionar todos os botões de detalhes
    const buttons = document.querySelectorAll('.view-details-btn');

    // 2. Elementos do Modal para manipular
    const modalTitle = document.getElementById('modalOrderTitle');
    const modalBody = document.getElementById('itemsTableContainer');
    const loader = document.getElementById('modalLoader');

    // 3. Adicionar evento de clique a cada botão
    buttons.forEach(button => {
        button.addEventListener('click', function () {
            const orderId = this.getAttribute('data-id');

            // Atualiza o Título
            modalTitle.textContent = orderId;

            // RESET: Mostra Loader, Esconde Tabela antiga
            loader.style.display = 'flex'; // ou 'block' dependendo do teu CSS
            modalBody.innerHTML = '';

            // 4. AJAX: Pedir os dados ao Flask
            fetch(`/order_details/${orderId}`) // Verifica se o teu prefixo da Blueprint é /shop ou /store
                .then(response => response.text()) // Queremos HTML (texto), não JSON
                .then(html => {

                    // Esconde Loader
                    loader.style.display = 'none';
                    // Injeta o HTML que veio do Python
                    modalBody.innerHTML = html;

                    var myModalEl = document.getElementById('detailsModal');
                    // Verifica se já existe uma instância do modal aberta para não duplicar
                    var modalInstance = bootstrap.Modal.getInstance(myModalEl);

                    if (!modalInstance) {
                        // Se não existir, cria uma nova
                        modalInstance = new bootstrap.Modal(myModalEl);
                    }

                    modalInstance.show();
                })
                .catch(error => {
                    console.error('Erro:', error);
                    modalBody.innerHTML = '<p class="text-danger">Erro ao carregar detalhes.</p>';
                    loader.style.display = 'none';
                });
        });
    });