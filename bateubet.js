const puppeteer = require('puppeteer');

(async () => {
  const readline = require('readline').createInterface({
    input: process.stdin,
    output: process.stdout
  });

  readline.question('Digite o CPF: ', async (cpf) => {
    const browser = await puppeteer.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const page = await browser.newPage();
    await page.goto('https://bateu.bet.br', { waitUntil: 'networkidle2' });

    // Clica no botão "Registre-se"
    await page.evaluate(() => {
      const spans = Array.from(document.querySelectorAll('span'));
      const target = spans.find(s => s.textContent.includes('Registre-se'));
      if (target) target.click();
    });

    // Espera o campo de CPF aparecer
    await page.waitForSelector('input[name="cpf"], input[placeholder*="CPF"]', { timeout: 10000 });

    // Preenche o CPF
    await page.type('input[name="cpf"], input[placeholder*="CPF"]', cpf);

    // Aguarda um tempo para os dados carregarem (ou evento ocorrer)
    await page.waitForTimeout(3000);

    // Tira o texto da página (como resposta visível)
    const bodyText = await page.evaluate(() => document.body.innerText);

    console.log("\n=== CONTEÚDO DA PÁGINA ===");
    console.log(bodyText);

    await browser.close();
    readline.close();
  });
})();