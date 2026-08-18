// Express middleware using jwks-rsa + jsonwebtoken
const jwt = require("jsonwebtoken");
const jwksClient = require("jwks-rsa");

const client = jwksClient({
  jwksUri: "https://auth.example.local/.well-known/jwks.json",
  cache: true,
  cacheMaxEntries: 5,
  cacheMaxAge: 10 * 60 * 1000
});

function getKey(header, callback){
  client.getSigningKey(header.kid, function(err, key) {
    if (err) return callback(err, null);
    const signingKey = key.getPublicKey();
    callback(null, signingKey);
  });
}

function verifyMiddleware(requiredCapability) {
  return function(req, res, next) {
    const auth = req.headers.authorization;
    if (!auth) return res.status(401).send("Missing Authorization");
    const token = auth.split(" ")[1];
    jwt.verify(token, getKey, { algorithms: ["RS256"], issuer: "https://auth.example.local" }, (err, decoded) => {
      if (err) return res.status(401).send(err.message);
      if (requiredCapability && !(decoded.capabilities || []).includes(requiredCapability)) {
        return res.status(403).send("Forbidden: missing capability");
      }
      req.user = decoded;
      next();
    });
  };
}

module.exports = verifyMiddleware;
