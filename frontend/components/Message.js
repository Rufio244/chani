export default function Message({ role, text }) {
  return (
    <div style={{
      textAlign: role === "user" ? "right" : "left",
      margin: "10px"
    }}>
      <div style={{
        display: "inline-block",
        padding: "10px",
        borderRadius: "10px",
        background: role === "user" ? "#007bff" : "#eee",
        color: role === "user" ? "#fff" : "#000"
      }}>
        {text}
      </div>
    </div>
  )
}
