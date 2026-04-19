export async function auth(req) {

  const token = req.headers.authorization;

  if (!token) return null;

  // simple validation (upgrade to JWT later)
  if (token === process.env.API_KEY) {
    return { id: "system-user" };
  }

  return null;
}
