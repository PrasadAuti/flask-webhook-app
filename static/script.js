document.addEventListener("DOMContentLoaded", () => {
  const webhookList = document.getElementById("webhook-list");
  const webhookDetails = document.getElementById("webhook-details");

  // Example: Fetch webhooks from API
  fetch("/api/webhooks")
    .then(res => res.json())
    .then(data => {
      data.forEach((hook, index) => {
        const li = document.createElement("li");
        li.textContent = `Webhook ${index + 1}`;
        li.addEventListener("click", () => {
          webhookDetails.textContent = JSON.stringify(hook, null, 2);
        });
        webhookList.appendChild(li);
      });
    });
});
