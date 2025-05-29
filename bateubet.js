const { chromium } = require('playwright'); // playwright funciona melhor no Termux

(async () => {
  const readline = require('readline').createInterface({
    input: process.stdin,
    output: process.stdout
  });

  readline.question('Digite o CPF: ', async (cpf) => {
    const browser = await chromium.launch({ headless: true }); // headless true funciona sem abrir interface
    const page = await browser.newPage();
    await page.goto('https://bateu.bet.br', { waitUntil: 'networkidle' });

    // Clica no botão "Registre-se"
    await page.locator('span', { hasText: 'Registre-se' }).click();

    // Espera e preenche o CPF
    await page.locator('input[placeholder*="CPF"]').fill(cpf);

    await page.waitForTimeout(3000); // espera possíveis dados carregarem

    const content = await page.content();
    console.log('\n=== HTML da página ===\n');
    console.log(content);

    await browser.close();
    readline.close();
  });
})();
