import { app } from "../../scripts/app.js";
import { ComfyWidgets } from "../../scripts/widgets.js";

// Shows the generated positive / negative prompt in read-only multiline fields
// directly on the "JDX 5. Generate Prompt" node. The text comes from the node's
// "ui" payload (see JDXGeneratePrompt.execute in comfy_nodes.py).

app.registerExtension({
    name: "JDXGenerator.ShowGeneratedText",

    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name !== "JDXGeneratePrompt") return;

        // Get an existing preview widget by name, or create a read-only one.
        function ensureWidget(node, name) {
            let w = node.widgets && node.widgets.find((x) => x.name === name);
            if (w) return w;

            w = ComfyWidgets["STRING"](
                node,
                name,
                ["STRING", { multiline: true }],
                app
            ).widget;

            if (w.inputEl) {
                w.inputEl.readOnly = true;
                w.inputEl.style.opacity = "0.75";
                w.inputEl.style.cursor = "text";
            }
            // Don't bloat the saved workflow with the generated text.
            w.serializeValue = async () => "";
            return w;
        }

        function setPreview(node, positive, negative) {
            const join = (v) => (Array.isArray(v) ? v.join("") : (v ?? ""));
            ensureWidget(node, "positive").value = join(positive);
            ensureWidget(node, "negative").value = join(negative);

            // Grow the node so both fields are visible.
            requestAnimationFrame(() => {
                const sz = node.computeSize();
                node.setSize([Math.max(node.size[0], sz[0]), Math.max(node.size[1], sz[1])]);
                node.setDirtyCanvas(true, true);
            });
        }

        // Create the (empty) fields as soon as the node is added.
        const onNodeCreated = nodeType.prototype.onNodeCreated;
        nodeType.prototype.onNodeCreated = function () {
            onNodeCreated?.apply(this, arguments);
            ensureWidget(this, "positive").value = "";
            ensureWidget(this, "negative").value = "";
        };

        // Fill them after each execution.
        const onExecuted = nodeType.prototype.onExecuted;
        nodeType.prototype.onExecuted = function (message) {
            onExecuted?.apply(this, arguments);
            setPreview(this, message?.positive, message?.negative);
        };
    },
});
