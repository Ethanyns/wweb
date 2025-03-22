const express = require("express");
const http = require("http");
const socketIo = require("socket.io");
const { Client } = require("whatsapp-web.js");
const cors = require("cors");

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

app.use(cors());
app.use(express.static("public")); // Serve webpage

const client = new Client();
let chatHistory = {}; // Store messages by chat ID

client.on("qr", (qr) => {
    console.log("Scan this QR code with WhatsApp:");
    io.emit("qr", qr);
});

client.on("ready", () => {
    console.log("WhatsApp Web is ready!");
    io.emit("ready");
});

client.on("message", async (msg) => {
    const chatId = msg.from;
    if (!chatHistory[chatId]) chatHistory[chatId] = [];
    chatHistory[chatId].push({ sender: msg.fromMe ? "You" : msg.from, text: msg.body });

    io.emit("newMessage", { chatId, sender: msg.fromMe ? "You" : msg.from, text: msg.body });
});

client.initialize();

app.get("/messages", (req, res) => {
    res.json(chatHistory);
});

server.listen(3000, () => console.log("Server running on port 3000"));
