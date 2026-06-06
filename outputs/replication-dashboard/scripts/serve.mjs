import { createReadStream, existsSync, statSync } from "node:fs";
import { createServer } from "node:http";
import { extname, join, normalize } from "node:path";

const root = process.cwd();
const port = Number(process.env.PORT || 4173);
const host = process.env.HOST || "127.0.0.1";

const mimeTypes = {
  ".css": "text/css",
  ".html": "text/html",
  ".js": "text/javascript",
  ".json": "application/json",
  ".svg": "image/svg+xml"
};

function resolvePath(url) {
  const cleanPath = normalize(decodeURIComponent(url.split("?")[0])).replace(/^(\.\.[/\\])+/, "");
  const candidate = join(root, cleanPath === "/" ? "index.html" : cleanPath);
  if (existsSync(candidate) && statSync(candidate).isDirectory()) {
    return join(candidate, "index.html");
  }
  return candidate;
}

createServer((request, response) => {
  const filePath = resolvePath(request.url || "/");
  const safeRoot = normalize(root);
  const safePath = normalize(filePath);

  if (!safePath.startsWith(safeRoot) || !existsSync(filePath)) {
    response.writeHead(404, { "Content-Type": "text/plain" });
    response.end("Not found");
    return;
  }

  response.writeHead(200, {
    "Content-Type": mimeTypes[extname(filePath)] || "application/octet-stream"
  });
  createReadStream(filePath).pipe(response);
}).listen(port, host, () => {
  console.log(`Replication dashboard running at http://${host}:${port}`);
});
