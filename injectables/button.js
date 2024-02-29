function createJobHiddenInput() {
    let hiddenInput = document.createElement('input');
    hiddenInput.type = 'hidden';
    hiddenInput.name = 'job_ids';
    hiddenInput.id = 'jca-job_ids';
    hiddenInput.value = '{"job_ids": []}';
    document.head.appendChild(hiddenInput);
}

function injectButtons() {
    // Get all div elements with 'data-job-id'
    const jobDivs = document.querySelectorAll('div[data-job-id]');

    jobDivs.forEach(div => {
        // Check if the button has already been injected
        if (!div.querySelector('.injected-button')) {
            // Create a new button
            const newButton = document.createElement('button');
            newButton.innerHTML = 'Add to search';
            newButton.className = 'injectable-button';  // Add a class to mark this button

            // Optional: Add event listener to the button
            newButton.addEventListener('click', function (event) {
                // Handle the button click event
                let jobId = div.getAttribute('data-job-id');
                let hiddenInput = document.getElementById('jca-job_ids');

                let currentJobIds = JSON.parse(hiddenInput.value);

                let exists = currentJobIds.job_ids.includes(jobId);

                if (exists) {
                    console.log('Job ID already exists:', jobId);
                    return;
                }

                currentJobIds.job_ids.push(div.getAttribute('data-job-id'));

                hiddenInput.value = JSON.stringify(currentJobIds);
            });

            // Append the button to the div
            div.appendChild(newButton);
        }
    });
}

// Create the hidden input
createJobHiddenInput();

// Set interval to run the function every X milliseconds
setInterval(injectButtons, 1000);  // Adjust the time as needed

