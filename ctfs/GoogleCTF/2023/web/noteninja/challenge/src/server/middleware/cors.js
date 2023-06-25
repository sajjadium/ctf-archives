const cors = (handler) => (req, res) => {
  const allowedOrigins = [];

  res.setHeader(
    "Access-Control-Allow-Origin",
    process.env.NODE_ENV === "development"
      ? "http://localhost:3000"
      : allowedOrigins.includes(req.headers.origin) && req.headers.origin
  );
  res.setHeader("Access-Control-Allow-Credentials", "true");
  res.setHeader(
    "Access-Control-Allow-Methods",
    "OPTIONS, GET, PATCH, DELETE, POST, PUT"
  );
  res.setHeader(
    "Access-Control-Allow-Headers",
    "Content-Type, Accept"
  );

  if (req.method === "OPTIONS") {
    return res.status(204).end();
  }

  return handler(req, res);
};

export default cors;
