"use client"
import { useState } from "react"
import Message from "./Message"
import { sendMessage, runComputer } from "../services/api"

export default function ChatBox() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState("")
  const [mode, setMode] = useState("agent") // agent | computer

  const handleSend = async () => {
    if (!input) return

    const userMsg = { role: "user", text: input }
    setMessages(prev => [...prev, userMsg])

    let res

    if (mode === "agent") {
      res = await sendMessage(input)
    } else {
      res = await runComputer(input)
    }

    const aiMsg = {
      role: "ai",
      text: JSON.stringify(res.data, null, 2)
    }

    setMessages(prev => [...prev, aiMsg])
    setInput("")
  }

  return (
    <div style={{ maxWidth: 800, margin: "auto" }}>
      <h2>Chani AI 💬</h2>

      <select onChange={(e) => setMode(e.target.value)}>
        <option value="agent">Agent</option>
        <option value="computer">Computer Control</option>
      </select>

      <div style={{
        height: "400px",
        overflowY: "auto",
        border: "1px solid #ccc",
        padding: "10px"
      }}>
        {messages.map((m, i) => (
          <Message key={i} role={m.role} text={m.text} />
        ))}
      </div>

      <div style={{ display: "flex", marginTop: 10 }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          style={{ flex: 1, padding: 10 }}
          placeholder="พิมพ์ข้อความ..."
        />
        <button onClick={handleSend}>ส่ง</button>
      </div>
    </div>
  )
}
