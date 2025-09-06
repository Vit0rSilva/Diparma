const boxPratos = document.querySelector('.box-pratos');

function verificarScroll() {
    if (boxPratos.scrollHeight > boxPratos.clientHeight) {
        boxPratos.classList.add('tem-scroll');
    } else {
        boxPratos.classList.remove('tem-scroll');
    }
}

// Rodar na inicialização
verificarScroll();

// Rodar toda vez que houver mudança de tamanho
window.addEventListener('resize', verificarScroll);


//Abrir modal
const modalCarrinho = document.querySelector('.modal-carrinho');
const carrinho = document.querySelector('.modal-conteudo-carrinho');
const body = document.body;


function abrirModal(){
    modalCarrinho.classList.add('ativo-modal');
    carrinho.classList.add('ativo-carrinho');
    body.classList.add('modal-aberto'); // bloqueia scroll
}


modalCarrinho.addEventListener('click', (e) => {
    if (e.target === modalCarrinho) {
        fecharModal();
    }
});

function fecharModal() {
    modalCarrinho.classList.remove('ativo-modal');
    carrinho.classList.remove('ativo-carrinho');
    body.classList.remove('modal-aberto'); // libera scroll
}

//Passando carrinho

function paginaFormaPagamento(){
    const previsao = document.querySelector('.box-endereco .previsao');
    const previsaoEditar = document.querySelector('.box-endereco .previsao-editar');
    const boxPratos = document.querySelector('.box-pratos');
    const boxSubTotal = document.querySelector('.box-sub-total');
    const buttonTotal = document.querySelector('.button-total');

    //Box endereço
    previsao.textContent = "Previsão de entrega";
    previsaoEditar.innerHTML = `<i class="ph ph-clock-countdown me-2"></i>
    <h2>22:45</h2>`;

    boxPratos.innerHTML = `<div class="prato-minimizado">
    <p>1 - Risoto de camarão</p>
    <p>R$77.43</p>
    </div><div class="prato-minimizado">
    <p>1 - Risoto de camarão</p>
    <p>R$77.43</p>
    </div><div class="prato-minimizado">
    <p>1 - Risoto de camarão</p>
    <p>R$77.43</p>
    </div>`;

    boxSubTotal.innerHTML = `<hr>

                <div class="radio-buttons">
                    <label class="radio-btn">
                        <input type="radio" name="opcao" value="1" checked>
                        <p>Cartão <i class="ph ph-credit-card"></i></p>
                    </label>
                    <label class="radio-btn">
                        <input type="radio" name="opcao" value="1">
                        <p>Dinheiro <i class="ph ph-credit-card"></i></p>
                    </label>
                    <label class="radio-btn">
                        <input type="radio" name="opcao" value="1">
                        <p>Pix <i class="ph ph-credit-card"></i></p>
                    </label>
                </div>
                <div class="forma-pagamento">
                    <!--
                    <input type="number" name="" id="" placeholder="Exemplo: R$24,00">
                    <div class="d-flex"><i class="ph ph-warning-circle alerta-cor"></i><p class="ms-2">O QR Code Pix vai ser gerado na hora da entrega</p></div>
                    -->
                    
                    <div class="d-flex align-items-center">
                        <input type="radio" name="cartao-forma" value="credito" id="credito">
                        <label for="credito">Credito</label>
                    </div>
                    <div class="d-flex align-items-center">
                        <input type="radio" name="cartao-forma" value="debito" id="debito">
                        <label for="debito">Debito</label>
                    </div>
                    <div class="d-flex align-items-center">
                        <input type="radio" name="cartao-forma" value="vale" id="vale">
                        <label for="vale">Vale-Alimentação</label>
                    </div>
                    
                </div>`;
    

}

const formaPagamento = document.querySelector('.radio-buttons input[name="opcao"]:checked').value;
if(formaPagamento){
    const boxFormaPagamento = document.querySelector('.forma-pagamento');
    if(formaPagamento === 'credito'){
        boxFormaPagamento.innerHTML = `
            <div class="d-flex align-items-center">
                <input type="radio" name="cartao-forma" value="credito" id="credito">
                <label for="credito">Credito</label>
            </div>
            <div class="d-flex align-items-center">
                <input type="radio" name="cartao-forma" value="debito" id="debito">
                <label for="debito">Debito</label>
            </div>
            <div class="d-flex align-items-center">
                <input type="radio" name="cartao-forma" value="vale" id="vale">
                <label for="vale">Vale-Alimentação</label>
            </div>
        `;
    }
    else if(formaPagamento === 'dinheiro'){
        boxFormaPagamento.innerHTML = `
            <input type="number" name="" id="" placeholder="Exemplo: R$24,00">
        `;
    }else if(formaPagamento === 'pix'){
        boxFormaPagamento.innerHTML = `
            <div class="d-flex"><i class="ph ph-warning-circle alerta-cor"></i><p class="ms-2">O QR Code Pix vai ser gerado na hora da entrega</p></div>
        `;
    }
}