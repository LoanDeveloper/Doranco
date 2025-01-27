const cluster = require('cluster');
const http = require('http');
const os = require('os');
const numCPUs = os.cpus().length;

if (cluster.isMaster) {
  // Création d'un processus worker pour chaque cœur du CPU
  console.log(`Le processus maître est ${process.pid}`);
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }

  cluster.on('exit', (worker, code, signal) => {
    console.log(`Le processus worker ${worker.process.pid} a terminé`);
  });
} else {
  // Serveur HTTP dans chaque worker
  http.createServer((req, res) => {
    res.writeHead(200);
    res.end(`Hello, World! Depuis le worker ${process.pid}`);
  }).listen(8000, () => {
    console.log(`Worker ${process.pid} en écoute sur le port 8000`);
  });
}