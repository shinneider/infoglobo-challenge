import app from './app';

const port = 3000; // process.env.PORT || 3000;
app.listen(port, err => {
  if (err) return console.log(err);
  return console.log(`Server running in port: ${port}`);
});
