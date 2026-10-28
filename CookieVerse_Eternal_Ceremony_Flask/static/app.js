const toast = document.getElementById("toast");
let toastTimer;
function showToast(message) {
  toast.textContent = message;
  toast.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove("show"), 2800);
}
document.getElementById("lightButton").addEventListener("click", () => {
  document.body.classList.toggle("celebrating");
  const active = document.body.classList.contains("celebrating");
  document.getElementById("lightButton").textContent = active ? "Celebration glowing ✨" : "Light the celebration ✨";
  showToast(active ? "The CookieVerse celebration is glowing! ✦" : "The lights have softly dimmed. ✧");
});
document.getElementById("oathButton").addEventListener("click", async () => {
  const button = document.getElementById("oathButton");
  const status = document.getElementById("oathStatus");
  const name = document.getElementById("runnerName").value.trim() || "Cookie Runner";
  const message = document.getElementById("oathMessage").value.trim();
  button.disabled = true;
  button.textContent = "Adding your sparkle…";
  status.textContent = "";
  try {
    const response = await fetch("/api/oath", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({name, message})
    });
    if (!response.ok) throw new Error("Could not save your message.");
    const data = await response.json();
    const empty = document.getElementById("emptyState");
    if (empty) empty.remove();
    const entry = document.createElement("article");
    entry.className = "entry";
    const avatar = document.createElement("div");
    avatar.className = "entry-avatar";
    avatar.textContent = "✦";
    const content = document.createElement("div");
    const title = document.createElement("h3");
    title.textContent = data.entry.name;
    const body = document.createElement("p");
    body.textContent = data.entry.message;
    const time = document.createElement("small");
    time.textContent = data.entry.time;
    content.append(title, body, time);
    entry.append(avatar, content);
    document.getElementById("entries").prepend(entry);
    document.getElementById("oathMessage").value = "";
    status.textContent = "Your promise has joined the guestbook. Thank you, Cookie Runner!";
    showToast("Your sparkle has been added to the CookieVerse ✦");
  } catch (error) {
    status.textContent = "We couldn't save that just now. Please try again.";
  } finally {
    button.disabled = false;
    button.textContent = "Make my promise ✦";
  }
});
