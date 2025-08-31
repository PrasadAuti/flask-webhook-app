(() => {
  const listEl = document.getElementById("webhook-list");
  const headersEl = document.getElementById("headers");
  const qparamsEl = document.getElementById("qparams");
  const payloadEl = document.getElementById("payload");
  const methodEl = document.getElementById("method");
  const receivedAtEl = document.getElementById("received_at");
  const detailTitle = document.getElementById("detail-title");
  const refreshBtn = document.getElementById("refresh-btn");
  const countEl = document.getElementById("count");

  let items = [];
  let selectedId = null;

  function pretty(obj) {
    try {
      return JSON.stringify(obj, null, 2);
    } catch {
      return String(obj);
    }
  }

  function renderList() {
    listEl.innerHTML = "";
    items.forEach((it) => {
      const li = document.createElement("li");
      li.className = "webhook-item";
      li.dataset.id = it.id;

      const left = document.createElement("div");
      left.className = "item-left";

      const badge = document.createElement("span");
      badge.className =
        "badge " + (it.method ? it.method.toLowerCase() : "post");
      badge.textContent = (it.method || "POST").toUpperCase();

      const meta = document.createElement("div");
      meta.className = "item-meta";
      const ts = it.received_at || "";
      const time = ts.split(" ")[1] || ts; // HH:MM:SS
      meta.textContent = time;

      left.appendChild(badge);
      left.appendChild(meta);

      // delete button
      const delBtn = document.createElement("button");
      delBtn.className = "delete-btn";
      delBtn.textContent = "×";
      delBtn.title = "Delete webhook";
      delBtn.addEventListener("click", async (e) => {
        e.stopPropagation(); // don’t trigger item select
        try {
          const res = await fetch(`/api/webhook/delete/${it.id}`, {
            method: "DELETE",
          });
          if (res.ok) {
            // remove from local list
            items = items.filter((x) => x.id !== it.id);
            renderList();
            if (selectedId === it.id) {
              selectedId = null;
              selectItem(null);
            }
          } else {
            console.error("Delete failed");
          }
        } catch (err) {
          console.error("Error deleting webhook", err);
        }
      });

      li.appendChild(left);
      li.appendChild(delBtn);

      li.addEventListener("click", () => {
        selectItem(it.id);
      });

      if (selectedId === it.id) {
        li.classList.add("active");
      }

      listEl.appendChild(li);
    });
    countEl.textContent = items.length;
  }

  function selectItem(id) {
    selectedId = id;
    const it = items.find((x) => String(x.id) === String(id));
    document.querySelectorAll(".webhook-item").forEach((el) => {
      el.classList.toggle("active", el.dataset.id === String(id));
    });

    if (!it) {
      detailTitle.textContent = "Select a webhook to view details";
      headersEl.textContent =
        qparamsEl.textContent =
        payloadEl.textContent =
          "—";
      methodEl.textContent = receivedAtEl.textContent = "—";
      return;
    }

    detailTitle.textContent = `Webhook #${items.indexOf(it) + 1}`;
    headersEl.textContent = pretty(it.headers || {});
    qparamsEl.textContent = pretty(it.query_params || {});
    try {
      payloadEl.textContent = pretty(JSON.parse(it.payload));
    } catch {
      payloadEl.textContent = it.payload || "(empty)";
    }
    methodEl.textContent = it.method || "—";
    receivedAtEl.textContent = it.received_at || "—";
  }

  async function load() {
    try {
      const res = await fetch("/api/webhooks");
      if (!res.ok) throw new Error("Failed to load");
      items = await res.json();
      renderList();
      if (items.length) selectItem(items[0].id);
    } catch (err) {
      console.error(err);
    }
  }

  refreshBtn.addEventListener("click", load);

  // initial load
  load();
})();
