const express = require('express');
const app = express();
app.use(express.json());

const products = [
  { id: 1, name: 'SecureShop T-shirt', price: 19.99 },
  { id: 2, name: 'SecureShop Mug', price: 12.95 },
  { id: 3, name: 'SecureShop Sticker', price: 3.5 }
];

app.get('/products', (req, res) => {
  res.json({ products });
});

app.get('/products/:id', (req, res) => {
  const product = products.find((item) => item.id === Number(req.params.id));
  if (!product) {
    return res.status(404).json({ error: 'product not found' });
  }
  res.json(product);
});

app.listen(8002, '0.0.0.0', () => {
  console.log('Product service listening on port 8002');
});
