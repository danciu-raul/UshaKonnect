//Transactions button pressed
function handleTransactionClick() {
  const statButton = document.querySelector('.btn-stat');
  const transButton = document.querySelector('.btn-transaction');

  const statDiv = document.querySelector('.statistics');
  const transDiv = document.querySelector('.transactions');

  statDiv.style.display = 'none';
  transDiv.style.display = 'block';

  transButton.style.border = '2px solid white';
  statButton.style.border = '2px solid transparent';
}

//Stats button pressed
function handleStatClick() {
  const statButton = document.querySelector('.btn-stat');
  const transButton = document.querySelector('.btn-transaction');

  const statDiv = document.querySelector('.statistics');
  const transDiv = document.querySelector('.transactions');

  statDiv.style.display = 'block';
  transDiv.style.display = 'none';

  transButton.style.border = '2px solid transparent';
  statButton.style.border = '2px solid white';
}
