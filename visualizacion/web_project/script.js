const images = [  'imagen1.jpg',  'imagen2.jpg',  'imagen3.jpg',  'imagen4.jpg',];

let counter = 0;

function showImage(index) {
  const container = document.getElementById('image-container');
  const imageName = `FiguraImport${counter}.png`;
  console.log('Nombre de la imagen:', imageName);
  container.style.backgroundImage = `url(imagenes/${imageName})`;
  //container.style.backgroundImage = `url(imagenes/FiguraImport1.png)`;
}

function previousImage() {
  if (counter > 0) {
    counter--;
    console.log('Nuevo valor del contador:', counter);
    showImage(counter);
  }
}

function nextImage() {
  console.log('images.length:', images.length);
  if (counter < images.length - 1) {
    counter++;
    console.log('Nuevo valor del contador:', counter);
    showImage(counter);
  }
}

document.getElementById('previous').addEventListener('click', previousImage);
document.getElementById('next').addEventListener('click', nextImage);


showImage();
