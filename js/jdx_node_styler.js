import { app } from "../../scripts/app.js";

// JDX Generator Cosmic Color Palette
const JDX_COLORS = {
    "JDXBaseConfig": { bgcolor: "#1a0b2e", title_color: "#b084f5" },
    "JDXCharacterModifiers": { bgcolor: "#0a1f2e", title_color: "#64b5f6" },
    "JDXClothingModifiers": { bgcolor: "#2e1a0b", title_color: "#ffb74d" },
    "JDXStyleModifiers": { bgcolor: "#0a2e16", title_color: "#81c784" },
    "JDXGeneratePrompt": { bgcolor: "#2e0a16", title_color: "#e57373" }
};

app.registerExtension({
    name: "JDXGenerator.CustomUI",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        // Only target JDX nodes
        if (nodeData.name in JDX_COLORS) {
            
            // Apply custom node colors on creation
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                
                // Set Colors
                const colors = JDX_COLORS[nodeData.name];
                this.color = colors.bgcolor;
                this.bgcolor = colors.bgcolor;
                
                // Add a handy button if this node has many boolean toggles
                // Check if any input contains "use_"
                const hasToggles = this.widgets && this.widgets.some(w => w.name && w.name.startsWith("use_"));
                
                if (hasToggles) {
                    this.addWidget("button", "Check All", null, () => {
                        for (let w of this.widgets) {
                            if (w.name && w.name.startsWith("use_")) {
                                w.value = true;
                            }
                        }
                    });
                    
                    this.addWidget("button", "Uncheck All", null, () => {
                        for (let w of this.widgets) {
                            if (w.name && w.name.startsWith("use_")) {
                                w.value = false;
                            }
                        }
                    });
                }
                
                return r;
            };
        }
    }
});
