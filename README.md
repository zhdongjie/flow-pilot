# Flow-Pilot Demo

This repository is a demo system that integrates the FlowPilot SDK.

## Usage

1. Ensure the SDK repo is available at `E:\Project\Python\flowpilot-sdk`.
2. Build the SDK:

```bash
cd E:\Project\Python\flowpilot-sdk
npm install
npm run build
```

3. Start the demo app:

```bash
cd E:\Project\Python\flow-pilot\frontend
npm install
npm run dev
```

Open: `http://localhost:5173`

The demo loads the SDK from:

```
../../flowpilot-sdk/dist/flowpilot.umd.js
```

---

## Notes

The demo system only adds `data-guide-id` markers. All guidance UI is provided by the SDK.
