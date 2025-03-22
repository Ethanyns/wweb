const express = require("express");
const http = require("http");
const { Server } = require("socket.io");
const puppeteer = require("puppeteer");
const cors = require("cors");

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
    cors: {
        origin: "*", // Allow all origins (change this if needed)
        methods: ["GET", "POST"]
    }
});

// Middleware
app.use(cors());
app.use(express.static("public")); // Serve the webpage

// WhatsApp Web Puppeteer
let browser, page;

async function startWhatsApp() {
    browser = await puppeteer.launch({
        headless: true,
        args: ["--no-sandbox", "--disable-setuid-sandbox"]
    });

    page = await browser.newPage();
    await page.goto("https://web.whatsapp.com");

    // Wait for QR Code to appear
    console.log("Waiting for QR Code scan...");
}

// Start WhatsApp on server start
startWhatsApp().catch(console.error);

// WebSocket communication
io.on("connection", (socket) => {
    console.log("User connected");

    socket.on("sendMessage", async (data) => {
        const { chatId, message } = data;
        await page.evaluate((chatId, message) => {
            let chat = Store.Chat.get(chatId);
            chat.sendMessage(message);
        }, chatId, message);
    });

    socket.on("disconnect", () => {
        console.log("User disconnected");
    });
});

// Start the server
const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
