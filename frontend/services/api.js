import axios from "axios"

const API = axios.create({
  baseURL: "http://localhost:3000/api"
})

export const sendMessage = (message) => {
  return API.post("/agent", { message })
}

export const runComputer = (message) => {
  return API.post("/computer", { message })
}
