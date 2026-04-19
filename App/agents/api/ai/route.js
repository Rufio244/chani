import OpenAI from "openai";

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

export async function POST(req) {
  const body = await req.json();

  const res = await openai.chat.completions.create({
    model: "gpt-4.1",
    messages: [{ role: "user", content: body.prompt }]
  });

  return Response.json({
    output: res.choices[0].message.content
  });
}
