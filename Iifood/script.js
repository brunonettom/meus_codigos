// Aguarda o carregamento completo do DOM
window.addEventListener('DOMContentLoaded', () => {
    // Seleciona o botão de localização
    const locationBtn = document.getElementById('location-btn');
    
    // Ao clicar no botão, exibe alerta para simular troca de endereço
    locationBtn.addEventListener('click', () => {
      alert('Aqui você poderia inserir um modal para trocar a localização.');
    });
  
    // Seleciona o botão de carrinho
    const cartBtn = document.getElementById('cart-btn');
    
    // Ao clicar no carrinho, exibe alerta simulado
    cartBtn.addEventListener('click', () => {
      alert('Carrinho de compras vazio.');
    });
  });