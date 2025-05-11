const { test, expect } = require('@playwright/test');
const testData = require('../data/test-data.json');

// Hardcoded values
const CHATBOT_URL = 'http://localhost:8080';
const CHAT_INPUT_SELECTOR = '#chat-input';
const SEND_BUTTON_SELECTOR = '#send-button';
const RESPONSE_CONTAINER = '#response-content-container';
const AUTH = {
    email: 'pankajgautam4869@yahoo.com',
    password: 'Openwebui@123'
};

// Method to capture all response paragraphs and combine them
async function captureFullResponse(page) {
    // Wait for the response container to be visible
    await page.waitForSelector(RESPONSE_CONTAINER);
    
    // Get all paragraph elements within the response container
    const paragraphs = await page.$$(`${RESPONSE_CONTAINER} div p`);
    
    // Initialize an array to store paragraph texts
    const paragraphTexts = [];
    
    // Extract text from each paragraph
    for (const paragraph of paragraphs) {
        const text = await paragraph.textContent();
        if (text && text.trim()) {
            paragraphTexts.push(text.trim());
        }
    }
    
    // Combine all paragraphs into a single string
    return paragraphTexts.join(' ');
}

test.describe('Chatbot Interaction Tests', () => {
    test.beforeEach(async ({ page }) => {
        // Navigate to the chatbot page before each test
        await page.goto(CHATBOT_URL);
        
        // Login before each test
        await page.fill('input[type="email"]', AUTH.email);
        await page.fill('input[type="password"]', AUTH.password);
        await page.click('button[type="submit"]');
        
        // Wait for login to complete
        await page.waitForURL(CHATBOT_URL);
    });

    test('Process test cases from test-data.json', async ({ page }) => {
        for (const testCase of testData.test_cases) {
            // Process English queries
            if (testCase.queries.en) {
                const query = testCase.queries.en.input;
                console.log(`\nProcessing Test Case: ${testCase.id} - ${testCase.name}`);
                console.log(`Input Query: ${query}`);

                // Type the query into the chat input
                await page.fill(CHAT_INPUT_SELECTOR, query);
                
                // Click the send button
                await page.click(SEND_BUTTON_SELECTOR);

                // Capture the full response using our new method
                const response = await captureFullResponse(page);
                console.log(`Response Content: ${response}`);

                // Validate response length
                const validation = testCase.queries.en.validation;
                expect(response.length).toBeGreaterThanOrEqual(validation.min_length);
                expect(response.length).toBeLessThanOrEqual(validation.max_length);

                // Validate required keywords
                for (const keyword of validation.required_keywords) {
                    expect(response.toLowerCase()).toContain(keyword.toLowerCase());
                }
            }

            // Process Arabic queries
            if (testCase.queries.ar) {
                const query = testCase.queries.ar.input;
                console.log(`\nProcessing Test Case: ${testCase.id} - ${testCase.name} (Arabic)`);
                console.log(`Input Query: ${query}`);

                // Type the query into the chat input
                await page.fill(CHAT_INPUT_SELECTOR, query);
                
                // Click the send button
                await page.click(SEND_BUTTON_SELECTOR);

                // Capture the full response using our new method
                const response = await captureFullResponse(page);
                console.log(`Response Content: ${response}`);

                // Validate response length
                const validation = testCase.queries.ar.validation;
                expect(response.length).toBeGreaterThanOrEqual(validation.min_length);
                expect(response.length).toBeLessThanOrEqual(validation.max_length);

                // Validate required keywords
                for (const keyword of validation.required_keywords) {
                    expect(response.toLowerCase()).toContain(keyword.toLowerCase());
                }
            }
        }
    });
}); 