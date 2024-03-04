function createJobHiddenInput() {
    let hiddenInput = document.createElement('input');
    hiddenInput.type = 'hidden';
    hiddenInput.name = 'job_ids';
    hiddenInput.id = 'jca-job_ids';
    hiddenInput.value = '[]';
    document.head.appendChild(hiddenInput);
}

function injectJobCountTotal() {
    let jobTotal = document.getElementById('jca-job_total');

    if (!jobTotal) {
        let jobTotalElement = document.createElement('div');
        jobTotalElement.id = 'jca-job_total';
        jobTotalElement.classList.add('jca-job-select-total');
        document.body.prepend(jobTotalElement);

        jobTotal = jobTotalElement;
    }

    let hiddenInput = document.getElementById('jca-job_ids');
    let totalJobsSelected = JSON.parse(hiddenInput.value).length;

    jobTotal.innerHTML = `Selected Jobs: ${totalJobsSelected}`;
}

function injectButtons() {

    injectJobCountTotal();
    const jobDivs = document.querySelectorAll('div[data-job-id]');

    jobDivs.forEach(div => {
        if (!div.querySelector('.injectable-button')) {
            let jobId = div.getAttribute('data-job-id');
            let hiddenInput = document.getElementById('jca-job_ids');

            const newButton = document.createElement('button');
            newButton.innerHTML = 'Add to search';
            newButton.className = 'injectable-button';  // Add a class to mark this button
            div.setAttribute('data-is-selected', 'false');

            let jobIds = JSON.parse(hiddenInput.value);
            if (jobIds.indexOf(jobId) !== -1) {
                div.style = 'background-color: #93ef2978 !important;';
                div.setAttribute('data-is-selected', 'true');
                newButton.innerHTML = 'Remove from search';
            }

            newButton.addEventListener('click', function (event) {
                let jobId = div.getAttribute('data-job-id');
                let hiddenInput = document.getElementById('jca-job_ids');

                let jobIds = JSON.parse(hiddenInput.value);

                if (div.getAttribute('data-is-selected') === 'true') {
                    div.setAttribute('data-is-selected', 'false');

                    // Remove the job ID from the list
                    let index = jobIds.indexOf(jobId);
                    jobIds.splice(index, 1);

                    div.style = '';
                    event.target.innerHTML = 'Add to search';
                } else {
                    if (jobIds.indexOf(jobId) !== -1) {
                        console.log('Job ID already exists:', jobId);
                        return;
                    }

                    div.setAttribute('data-is-selected', 'true');

                    jobIds.push(div.getAttribute('data-job-id'));
                    div.style = 'background-color: #93ef2978 !important;';

                    event.target.innerHTML = 'Remove from search';
                }

                hiddenInput.value = JSON.stringify(jobIds);
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

