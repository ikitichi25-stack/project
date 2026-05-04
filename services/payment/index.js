const express = require('express');
const app = express();
app.use(express.json());

app.post('/pay', (req, res) => {
  const { amount, method } = req.body;
  if (!amount || !method) {
    return res.status(400).json({ error: 'amount and method are required' });
  }
  res.json({ status: 'payment accepted', amount, method });
});

app.listen(8004, '0.0.0.0', () => {
  console.log('Payment service listening on port 8004');
});
