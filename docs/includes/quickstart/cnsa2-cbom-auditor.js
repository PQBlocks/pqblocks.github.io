import { scanToCbom, verifyCbom } from '@pqblocks/cnsa2-cbom-auditor';

// Audit target directory and synthesize CycloneDX 1.6 CBOM
const { bom, summary } = await scanToCbom('./certs');
console.log('Inspected assets:', summary.total);
console.log('CycloneDX spec version:', bom.specVersion);

// Validate CBOM against CycloneDX 1.6 schema
const report = verifyCbom(bom);
console.log('Schema valid:', report.valid);
