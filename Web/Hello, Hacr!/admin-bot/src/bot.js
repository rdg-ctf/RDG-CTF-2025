const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: [
      '--no-sandbox', 
      '--disable-setuid-sandbox', 
      '--disable-dev-shm-usage',
      '--disable-gpu',
      '--window-size=1280x1024',
      '--disable-software-rasterizer',
      '--remote-debugging-port=9222',
      '--no-zygote',
      '--single-process',
      '--disable-extensions',
      '--disable-background-timer-throttling',
      '--disable-backgrounding-occluded-windows',
    ],
    userDataDir: '/tmp/puppeteer',
    ignoreHTTPSErrors: true,
  });

  const page = await browser.newPage();

  await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36');
  await page.setViewport({ width: 1280, height: 1024 });

  await page.goto('http://web:5000/login', { waitUntil: 'load' });

  await page.waitForSelector('input[name="username"]');
  await page.type('input[name="username"]', 'admin');
  await page.type('input[name="password"]', 'ipuhdfgsipuhbvfipujndfgsiuph');

  await Promise.all([
    page.waitForNavigation({ waitUntil: 'domcontentloaded' }),
    page.click('button[type="submit"]')
  ]);

  console.log('Авторизация прошла успешно!');

  async function declinePosts() {
    try {
      await page.goto('http://web:5000/admin', { waitUntil: 'domcontentloaded' });

      const postNumbers = await page.$$eval('ul li a', links =>
        links.map(link => link.href.match(/\/admin\/article\/(\d+)/)?.[1]).filter(Boolean)
      );

      if (postNumbers.length === 0) {
        console.log('Посты не найдены, ждем появления новых...');
        return false;
      }

      for (const postNumber of postNumbers) {
        console.log(`Посещение статьи #${postNumber}`);

        await page.goto(`http://web:5000/admin/article/${postNumber}`, { waitUntil: 'domcontentloaded' });

        console.log(`Отправляем запрос на отклонение...`);

        await page.evaluate(async (postNumber) => {
          await fetch(`/admin/decline_article/${postNumber}`, {
              method: 'POST'
          });
      }, postNumber);
      console.log(`Статья ${postNumber} отклонена!`);
  }

      return true;
    } catch (error) {
      console.error('Ошибка при обработке постов:', error);
      return false;
    }
  }

  async function monitorPosts() {
    while (true) {
      const postsDeclined = await declinePosts();

      if (!postsDeclined) {
        console.log('Ожидание новых постов...');
        try {
          await Promise.race([
            page.waitForSelector('ul li a', { visible: true, timeout: 0 }),
            new Promise(resolve => setTimeout(resolve, 10000)).then(async () => {
              console.log('Прошло 10 секунд, обновляем страницу...');
              await page.reload();
            })
          ]);
        } catch (error) {
          console.error('Ошибка ожидания постов:', error);
        }
      }
    }
  }

  await monitorPosts();
})();