const newFormScreen = document.getElementById('new-form-screen');
  const aiOptionButton = document.getElementById('ai-option-button');
  const enterFormNameScreen = document.getElementById('enter-form-name-screen');
  const formNameInput = document.getElementById('form-name-input');
  const createFormButton = document.getElementById('create-form-button');
  const loadingIndicator = document.getElementById('loading-indicator');
  const resultArea = document.getElementById('result-area');

  // Event listener for the "AI Form Generator" button
  aiOptionButton.addEventListener('click', () => {
    newFormScreen.style.display = 'none';
    enterFormNameScreen.style.display = 'block';
    resultArea.innerHTML = ''; // Clear previous results
    formNameInput.value = ''; // Clear previous input
    formNameInput.focus(); // Set focus to the input field
  });

  // Event listener for the "Create Form" button
  createFormButton.addEventListener('click', async () => {
    const formName = formNameInput.value.trim();
    if (formName === "") {
      // Use a more user-friendly way to indicate empty input, maybe a border highlight
      alert("Please enter a form name."); // Keeping alert for simplicity in this environment
      formNameInput.focus();
      return;
    }

    // Clear previous results before starting
    resultArea.innerHTML = '';

    // Show loading indicator and disable button
    loadingIndicator.style.display = 'block';
    createFormButton.disabled = true;


    try {

    try {
      const response = await fetch('YOUR_BACKEND_URL/create_form', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ form_name: formName }),
      });

      if (!response.ok) {
        // Handle non-200 HTTP responses
        const errorText = await response.text(); // Get error message from response body
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
      }

      const data = await response.json(); // Parse the JSON response

      // Process the response based on instructions
      if (data.status === 'success') {
        const formUrl = data.form_url;
        const successMessage = document.createElement('p');
        successMessage.className = 'success'; // Add success class for styling
        successMessage.textContent = "Form created successfully! Your form preview link is:";

        const formLink = document.createElement('a');
        formLink.href = formUrl;
        formLink.textContent = formUrl;
        formLink.target = "_blank"; // Open link in a new tab

        resultArea.appendChild(successMessage);
        resultArea.appendChild(formLink);

      } else if (data.status === 'failure') {
        const errorMessage = data.error || "Unknown error during form creation.";
        const errorElement = document.createElement('p');
        errorElement.className = 'error'; // Add error class for styling
        errorElement.textContent = `Form creation failed: ${errorMessage}`;
        resultArea.appendChild(errorElement);
      } else {
         // Handle cases where response data is not as expected
         const errorElement = document.createElement('p');
         errorElement.className = 'error'; // Add error class for styling
         errorElement.textContent = "An unexpected response format was received from the server.";
         resultArea.appendChild(errorElement);
      }

    } catch (e) {
      console.error("Error during form creation fetch:", e);
      const errorElement = document.createElement('p');
      errorElement.className = 'error'; // Add error class for styling
      errorElement.textContent = `An error occurred while creating the form: ${e}`;
      resultArea.appendChild(errorElement);
    } finally {
      // Hide loading indicator and re-enable button
      loadingIndicator.style.display = 'none';
      createFormButton.disabled = false;
    }
    
} finally {
      // Hide loading indicator and re-enable button
      loadingIndicator.style.display = 'none';
      createFormButton.disabled = false;
    }
  });