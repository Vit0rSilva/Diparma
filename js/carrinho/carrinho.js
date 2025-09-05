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

function formaPagamento(){
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

    boxSubTotal.innerHTML = '';
    

}