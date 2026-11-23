const {
  scan,
  scanToCbom,
  scanTarget,
  generateCbom,
  verifyCbom,
  compareCboms,
  classify
} = require('@pqblocks/cnsa2-cbom-auditor');

// 1. Scan a directory of certificates
async function runAudit() {
  const result = await scanToCbom('./golden-vectors', {
    maxFiles: 1000,
    failOn: 'disallowed'
  });

  console.log('Total Assets Found:', result.summary.total);
  console.log('Compliant Assets:', result.summary.compliant);
  console.log('Disallowed Assets:', result.summary.disallowed);

  // 2. Access the CycloneDX 1.6 BOM object
  const bom = result.bom;
  console.log('CycloneDX BOM Format:', bom.bomFormat); // "CycloneDX"
  console.log('Spec Version:', bom.specVersion);       // "1.6"

  // 3. Verify the generated CBOM
  const verification = verifyCbom(bom);
  console.log('CBOM Valid against Schema:', verification.valid);

  // 4. Classify an individual asset
  const sampleAsset = result.assets[0];
  const verdict = classify(sampleAsset);
  console.log(`Asset ${sampleAsset.file}: status=${verdict.verdict}, reason=${verdict.reason}`);
}

runAudit().catch(console.error);
