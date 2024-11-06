// Function to preview the uploaded image
function previewImage(event) {
  const file = event.target.files[0];
  const previewContainer = document.getElementById('imagePreview');
  previewContainer.innerHTML = ""; // Clear any existing content
  
  if (file) {
      const reader = new FileReader();
      reader.onload = function(e) {
          // Create an img element and set its src to the file content
          const imgElement = document.createElement('img');
          imgElement.src = e.target.result;
          imgElement.style.width = '200px'; // Set the preview size
          previewContainer.appendChild(imgElement);
      }
      reader.readAsDataURL(file); // Read the file as a data URL
  } else {
      previewContainer.innerHTML = "<p>No image uploaded yet.</p>";
  }
}


async function search(event) {
  event.preventDefault(); // Prevent form submission

  // Get the form data from the image search form
  var fileinput = document.getElementById("image").files[0]; // Get the selected file directly
  var tag = document.getElementById("tag").value;
  console.log(tag);

  const imageRequested = {
      'image': fileinput,
      'tag' : tag,
  };

  // Create a FormData object and append the image file
  const requestData = new FormData();
  requestData.append('image', fileinput); // Use the key 'image' for appending
  requestData.append('tag', tag);

  try {
      const response = await fetch('/Search_image', {
          method: "POST",
          body: requestData,
      });

      if (response.ok) {
          const jsonResponse = await response.json();
          display(jsonResponse.similar_images); // Ensure this matches your backend response
      } else {
          console.error('Error:', response.statusText);
      }
  } catch (error) {
      console.error('Error fetching data:', error);
  }
}

function display(images) {
  const resultDiv = document.getElementById('result');
  resultDiv.innerHTML = ""; // Clear previous results

  // Check if there are images to display
  if (!images || images.length === 0) {
      resultDiv.innerHTML = "<p>No similar images found.</p>";
      return;
  }

  const imageHtml = images.map(img => {
      return `<img src="/static/images/${img}" alt="Similar images" style="width:100px; margin: 10px;">`; // Fixed template literal
  }).join('');

  resultDiv.innerHTML = imageHtml; // Display the images
}

// Make sure to bind the search function correctly to the form's submit event in your HTML
document.getElementById("imageSearchForm").addEventListener("submit", search); 