require("dotenv").config();
const express = require("express");
const axios = require("axios");

const app = express();
app.use(express.json());

/**
 * 🔐 API KEYS (ใส่ใน .env)
 */
const OPENAI_KEY = process.env.OPENAI_API_KEY;
const GEMINI_KEY = process.env.GEMINI_API_KEY;

/**
 * 🧠 Memory (จำความสามารถ)
 */
let chaniMemory = {
  history: [],
  skills: []
};

/**
 * 🌐 AI CONNECTORS
 */
async function callOpenAI(prompt) {
  const res = await axios.post(
    "https://api.openai.com/v1/chat/completions",
    {
      model: "gpt-4o-mini",
      messages: [{ role: "user", content: prompt }]
    },
    {
      headers: {
        Authorization: `Bearer ${OPENAI_KEY}`
      }
    }
  );

  return res.data.choices[0].message.content;
}

async function callGemini(prompt) {
  const res = await axios.post(
    `https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${GEMINI_KEY}`,
    {
      contents: [{ parts: [{ text: prompt }] }]
    }
  );

  return res.data.candidates[0].content.parts[0].text;
}

/**
 * 🔄 NORMALIZER
 */
function normalizeOutput(source, output) {
  return {
    source,
    output,
    timestamp: new Date()
  };
}

/**
 * 🧠 CAPABILITY ENGINE
 */
function enhanceWithChani(outputs) {
  const combined = outputs.map(o => o.output).join("\n");

  const insight = {
    summary: combined.slice(0, 300),
    intelligence_score: Math.random() * 100
  };

  return insight;
}

/**
 * 📚 SKILL BUILDER
 */
function updateSkills(insight) {
  chaniMemory.skills.push({
    learned: insight.summary,
    score: insight.intelligence_score
  });
}

/**
 * 🚀 MAIN API
 */
app.post("/chani/execute", async (req, res) => {
  const { prompt, use = ["openai", "gemini"] } = req.body;

  try {
    let results = [];

    if (use.includes("openai")) {
      const out = await callOpenAI(prompt);
      results.push(normalizeOutput("openai", out));
    }

    if (use.includes("gemini")) {
      const out = await callGemini(prompt);
      results.push(normalizeOutput("gemini", out));
    }

    // 🧠 วิเคราะห์รวม
    const insight = enhanceWithChani(results);

    // 📚 อัปเกรดตัวเอง
    updateSkills(insight);

    // 💾 จำ
    chaniMemory.history.push({
      prompt,
      results,
      insight
    });

    res.json({
      success: true,
      chani: {
        insight,
        learned_skills: chaniMemory.skills.length
      },
      raw: results
    });

  } catch (err) {
    res.status(500).json({
      error: err.message
    });
  }
});

/**
 * 📡 RUN SERVER
 */
app.listen(3000, () => {
  console.log("🔥 Chani AI Unified API running on port 3000");
});
