function analyzeResume() {
    // Get the input elements
    const resumeInput = document.getElementById('resume');
    const jobDescSelect = document.getElementById('jobDesc'); // Changed to select
    // const skillsInput = document.getElementById('skills');

    // Get the values of the inputs
    const resumeFile = resumeInput.files[0];
    const jobDescValue = jobDescSelect.value; // Get the selected job description
    // const skillsValue = skillsInput.value;

    // TODO: Implement the logic to analyze the resume and job description
    // For demonstration purposes, we'll simulate the analysis results
    const matchScore = 85; // Example matching score
    const matchedSkills = ['JavaScript', 'Python']; // Example matched skills
    const suggestions = ['Add SQL to your resume for a higher match.']; // Example suggestions

    // Update the result div with the analysis results
    const resultDiv = document.getElementById('result');
    resultDiv.style.display = 'block';
    document.getElementById('matchScore').innerHTML = `Matching Score: <strong>${matchScore}%</strong>`;
    //document.getElementById('matchedSkills').innerHTML = `Matched Skills: <strong>${matchedSkills.join(', ')}</strong>`;
    document.getElementById('suggestions').innerHTML = `Suggestions: ${suggestions[0]}`;

    // search box

    document.getElementById('searchSkills').addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const searchTerms = searchTerm.split(',').map(term => term.trim()).filter(term => term); // Split by commas, trim, and filter out empty terms
        const rows = document.querySelectorAll('#matching-table-body tr');
    
        // Check if there are any search terms
        if (searchTerms.length === 0) {
            // If no search terms, show all rows
            rows.forEach(row => {
                row.style.display = ''; // Show all rows
            });
        } else {
            // If there are search terms, filter rows based on matches
            rows.forEach(row => {
                const skills = row.cells[1].textContent.toLowerCase();
                let matchesAll = true; // Assume it matches all terms initially
    
                // Check if all search terms match the skills
                searchTerms.forEach(term => {
                    if (!skills.includes(term)) {
                        matchesAll = false; // If any term does not match, set to false
                    }
                });
    
                // Show or hide the row based on matches
                if (matchesAll) {
                    row.style.display = ''; // Show row
                } else {
                    row.style.display = 'none'; // Hide row
                }
            });
        }
    });

}

let experienceColumnAdded = false;

const toggleColumnBtn = document.getElementById('toggle-column-btn');
toggleColumnBtn.addEventListener('click', function() {
    if (!experienceColumnAdded) {
        const tableBody = document.getElementById('matching-table-body');
        const rows = tableBody.rows;
        for (let i = 0; i < rows.length; i++) {
            const row = rows[i];
            const experienceCell = row.querySelector('#experience-cell');
            experienceCell.style.display = 'table-cell';
        }
        document.getElementById('experience-column').style.display = 'table-cell';
        toggleColumnBtn.textContent = '-';
        experienceColumnAdded = true;
    } else {
        const tableBody = document.getElementById('matching-table-body');
        const rows = tableBody.rows;
        for (let i = 0; i < rows.length; i++) {
            const row = rows[i];
            const experienceCell = row.querySelector('#experience-cell');
            experienceCell.style.display = 'none';
        }
        document.getElementById('experience-column').style.display = 'none';
        toggleColumnBtn.textContent = '+';
        experienceColumnAdded = false;
    }
});