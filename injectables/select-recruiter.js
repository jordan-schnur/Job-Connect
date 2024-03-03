function createJobHiddenInput() {
    let hiddenInput = document.createElement('input');
    hiddenInput.type = 'hidden';
    hiddenInput.name = 'jca-recruiter_profile_url';
    hiddenInput.id = 'jca-recruiter_profile_url';
    document.head.appendChild(hiddenInput);
}

function injectButtons() {
    // Get all div elements with 'data-job-id'
    const recruiterIds = document.querySelectorAll('section.org-people-profile-card');

    recruiterIds.forEach(section => {
        // Check if the button has already been injected
        if (!section.querySelector('.recruiter-button')) {
            // Create a new button
            const newButton = document.createElement('button');
            newButton.className = 'artdeco-button artdeco-button--2 artdeco-button--secondary ember-view full-width recruiter-button';
            newButton.style = 'margin-bottom: 10px;';
            const span = document.createElement('span');
            span.className = 'artdeco-button__text';
            span.innerHTML = 'Select For Search';
            newButton.appendChild(span);
            //TODO: On Select:
            // box-sizing: border-box;
            // border: 5px solid red !important;
            // box-shadow: inset 0 0 10px red !important;

            // Optional: Add event listener to the button
            newButton.addEventListener('click', function (event) {
                // Handle the button click event
                let recruiterProfileUrl = section.querySelector('a').getAttribute('href');
                let hiddenInput = document.getElementById('jca-recruiter_profile_url');

                let shouldContinue = false;
                if (hiddenInput.value !== '') {
                    shouldContinue = confirm('Are you sure you want to add this recruiter to the search?');

                    if (!shouldContinue) {
                        return;
                    }
                }

                hiddenInput.value = recruiterProfileUrl;
            });

            // Append the button to the div
            section.appendChild(newButton);
        }
    });
}

// Create the hidden input
createJobHiddenInput();

// Set interval to run the function every X milliseconds
setInterval(injectButtons, 1000);  // Adjust the time as needed

