package verifiers

import (
  "context"
  "time"
  "errors"
  "github.com/golang-jwt/jwt/v4"
  "github.com/MicahParks/keyfunc"
)

func VerifyToken(tokenString string, reqCap string) (jwt.MapClaims, error) {
  jwksURL := "https://auth.example.local/.well-known/jwks.json"
  ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
  defer cancel()
  jwks, err := keyfunc.Get(jwksURL, keyfunc.Options{RefreshInterval: time.Minute * 5})
  if err != nil {
    return nil, err
  }
  token, err := jwt.Parse(tokenString, jwks.Keyfunc)
  if err != nil || !token.Valid {
    return nil, err
  }
  claims, ok := token.Claims.(jwt.MapClaims)
  if !ok {
    return nil, errors.New("invalid claims")
  }
  if reqCap != "" {
    capsIfc, ok := claims["capabilities"].([]interface{})
    if !ok { return nil, errors.New("no capabilities") }
    found := false
    for _, c := range capsIfc {
      if s, ok := c.(string); ok && s == reqCap { found = true; break }
    }
    if !found { return nil, errors.New("missing capability") }
  }
  return claims, nil
}
