const express = require('express');
const mongoose = require('mongoose');
const app = express();

app.use(express.json()); // Para ler o corpo da requisição no formato JSON

mongoose.connect('mongodb://localhost:27017/dicionario', {
  useNewUrlParser: true,
  useUnifiedTopology: true
});

const Term = mongoose.model('Term', new mongoose.Schema({
  letter: String,
  term: String,
  definition: String
}));

app.post('/addTerm', async (req, res) => {
  const { letter, term, definition } = req.body;

  const newTerm = new Term({
    letter,
    term,
    definition
  });

  try {
    await newTerm.save();
    res.status(201).send({ message: 'Termo adicionado com sucesso!' });
  } catch (error) {
    res.status(500).send({ message: 'Erro ao adicionar termo.' });
  }
});

app.listen(3000, () => {
  console.log('Servidor rodando na porta 3000');
});
