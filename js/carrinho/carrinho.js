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

function paginaCarrinho($numero){
    const boxModal = document.querySelector('.modal-conteudo-carrinho');
    const previsao = document.querySelector('.box-endereco .previsao');
    const previsaoEditar = document.querySelector('.box-endereco .previsao-editar');
    const boxPratos = document.querySelector('.box-pratos');
    const boxSubTotal = document.querySelector('.box-sub-total');
    const buttonTotal = document.querySelector('.button-total');

    if($numero == 1){
        //Box endereço
        previsao.textContent = "";
        previsaoEditar.innerHTML = `<i class="ph ph-motorcycle me-3"></i>
        <p>20m-30m</p>`;
    
        boxPratos.innerHTML = `                <div class="prato">
        <div class="img-prato">
            <img src="img/risoto.png" alt="">
        </div>
        <div class="info-prato">
            <p>Risoto de Camarão</p>
            <div class="d-flex align-items-center">
                <i class="ph ph-users-four me-1"></i>
                <p class="legenda">2 pessoas</p>
            </div>
            <div class="adcionais">
                <i class="ph ph-plus me-2"></i>
                <div class="adcionais-p">
                    <p class="legenda">Camarões Salteados 100gr <span class="primary-apoio-cor">R$34,90</span></p>
                    <p class="legenda">Camarões Salteados 100gr <span class="primary-apoio-cor">R$34,90</span></p>
                    <p class="legenda">Camarões Salteados 100gr <span class="primary-apoio-cor">R$34,90</span></p>
                </div>
            </div>
        </div>
        <div class="preco ">
            <h2>R$76.99</h2>
            <div class="d-flex mt-auto justify-content-between">
                <select name="select">
                    <option value="valor1">1</option>
                    <option value="valor2" selected><p>20</p></option>
                    <option value="valor3">3</option>
                  </select>
                <button class="d-flex align-items-center"><i class="ph ph-trash"></i></button>
            </div>
        </div>
    </div>
    <div class="prato">
        <div class="img-prato">
            <img src="img/risoto.png" alt="">
        </div>
        <div class="info-prato">
            <p>Risoto de Camarão</p>
            <div class="d-flex align-items-center">
                <i class="ph ph-users-four me-1"></i>
                <p class="legenda">2 pessoas</p>
            </div>
            <div class="adcionais">
                <i class="ph ph-plus me-2"></i>
                <div class="adcionais-p">
                    <p class="legenda">Camarões Salteados 100gr <span class="primary-apoio-cor">R$34,90</span></p>
                    <p class="legenda">Camarões Salteados 100gr <span class="primary-apoio-cor">R$34,90</span></p>
                    <p class="legenda">Camarões Salteados 100gr <span class="primary-apoio-cor">R$34,90</span></p>
                </div>
            </div>
        </div>
        <div class="preco ">
            <h2>R$76.99</h2>
            <div class="d-flex mt-auto justify-content-between">
                <select name="select">
                    <option value="valor1">1</option>
                    <option value="valor2" selected><p class="">20</p></option>
                    <option value="valor3">3</option>
                  </select>
                <button class="d-flex align-items-center"><i class="ph ph-trash"></i></button>
            </div>
        </div>
    </div>`;
    
        boxSubTotal.innerHTML = `<hr>
        <div class="d-flex justify-content-between">
            <p>Sub Total</p>
            <p>R$150.00</p>
        </div>
        <div class="d-flex justify-content-between">
            <p>Frete</p>
            <p>R$8</p>
        </div>
        <div class="box-cupom">
            <p>Encontrar promoções</p>
            <button><i class="ph ph-ticket"></i><p>Adcionar cupom</p></button>
        </div>`;
        
        buttonTotal.classList.add('button-expandido')
        buttonTotal.innerHTML = `
            <button class="button-proximo" onclick="paginaCarrinho(2)"><p>Finalizar pedido</p><i class="ph ph-arrow-right ms-2"></i></div></button>
        `;
    }else if($numero == 2){
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
                            <input type="radio" name="opcao" onclick="formaPagamento()" value="cartao" checked>
                            <p>Cartão <i class="ph ph-credit-card"></i></p>
                        </label>
                        <label class="radio-btn">
                            <input type="radio" name="opcao" onclick="formaPagamento()" value="dinheiro">
                            <p>Dinheiro <i class="ph ph-credit-card"></i></p>
                        </label>
                        <label class="radio-btn">
                            <input type="radio" name="opcao" onclick="formaPagamento()" value="pix">
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
        
    
        buttonTotal.classList.add('button-metade');
        buttonTotal.classList.remove('button-expandido');
        buttonTotal.innerHTML = `
            <button class="button-border" onclick="paginaCarrinho(1)"><p>Voltar</p><i class="ph ph-arrow-left ms-2"></i></div></button>
            <button class="" onclick="paginaCarrinho(3)"><p>Finalizar pedido</p><i class="ph ph-arrow-right ms-2"></i></div></button>
        `;
    }else if(3){
        boxModal.innerHTML = `
        <div class="d-flex align-items-center mb-3">
            <h1>Cesta</h1>
            <i class="ph ph-tote ms-3"></i>
        </div>
        <div class="box-finalizado">
            <div class="centro">
                <h2>Pedido feito som sucesso</h2>
                <dotlottie-wc
                src="https://lottie.host/87d66e57-b196-4b6c-815c-3ead1bb282f8/QyzVWlvBx7.lottie"
                style="width: 300px;height: 300px"
                speed="1"
                autoplay
                ></dotlottie-wc>
            </div>
        </div>
        `;
    }

}

function formaPagamento(){
    console.log("oiii")
    const formaPagamento = document.querySelector('.radio-buttons input[name="opcao"]:checked').value;
    if(formaPagamento){
        const boxFormaPagamento = document.querySelector('.forma-pagamento');
        if(formaPagamento === 'cartao'){
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
}