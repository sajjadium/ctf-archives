import puppeteer from "puppeteer";

export function validVIN(vin) {
    const validCharset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    return typeof (vin) === "string" && vin.length === 17 && vin.split("").every(c => validCharset.includes(c));
}

export async function toPDF(html, style, options) {
    // we don't have the money to save all these reports...
    try {
        const opts = {
            ...options,
            path: undefined,
        };
        const stylePath = `/css/${style}.css`;
        const browser = await puppeteer.launch({ 
            headless: 'new',
            args: ["--no-sandbox", "--disable-setuid-sandbox"],
            executablePath: process.env.CHROME_BIN || undefined,
        });
        const page = await browser.newPage();
        await page.setContent(html);
        // try {
        //     await new Promise((resolve, reject) => {
        //         setTimeout(() => {
        //             reject("neither load nor error were fired");
        //         }, 5 * 1000);
        //         page.addStyleTag({
        //             url: stylePath,
        //         }).then(resolve).catch(reject);
        //     });
        // } catch (e) {
        //     await page.addStyleTag({
        //         url: "/css/formal.css"
        //     });
        // }
        console.log("pdf-ing")
        console.log(opts)
        const pdf = await page.pdf(opts);
        console.log("pdf-ing done")
        await page.close();
        await browser.close();
        return pdf;
    } catch (e) {
        console.error(e);
        return null;
    }
}

export function parseStringAsValue(s) {
    if (s === "true") {
        return true;
    } else if (s === "false") {
        return false;
    } else if (!isNaN(s)) {
        return Number(s);
    } else {
        return s;
    }
}

export function findPlateIndices(plates) {
    /*
        Our plates are of the format X111XX, which means there are 10^3 * 26^2 = 1000 * 676 possible plates.
        To save space, we give each plate an unique index, based on its alphabetical order in the list of all possible plates.

        This function takes a list of plates and finds these indices
    */
   const NUM_POS = 5;
   return plates.map(plate => {
        // remove the first char; we know its L
        const leftover = plate.substring(1);
        return leftover.split("").reduce((acc, c, i) => {
            if (isNaN(c)) {
                return acc + (NUM_POS - i) * (c.charCodeAt(i) - "A".charCodeAt(0));
            } else {
                return acc + (NUM_POS - i) * (c.charCodeAt(i) - "0".charCodeAt(0));
            }
        }, 0);
   });
}