import creator from './creator';
import extractor from './extractor';
import builder from './builder';
import {error} from '@pyanalyzer/logging';
import {CaseContainer} from '@pyanalyzer/doc-parser';
import {UNIMatcher} from '../../../matchers';
import {readFile} from 'node:fs/promises';

export default async (g: string, c: string, cs: CaseContainer, ocwd: string, exepath: string) => {
  try {
    const sym_data = await readFile(`${process.cwd()}/tests/pysonar2/${g}/${c}/${c}-sym.json`, 'utf-8');
    const ref_data = await readFile(`${process.cwd()}/tests/pysonar2/${g}/${c}/${c}-ref.json`, 'utf-8');
    // console.log(data.replaceAll(/\s+/g, ' '));
    builder(sym_data, ref_data, g, c);
    return UNIMatcher(cs, 'python', 'pysonar2');
  } catch {
    if (await creator(g, c, exepath)) {
      // const data = await extractor(g, c, ocwd);
      const sym_data = await readFile(`${process.cwd()}/tests/pysonar2/${g}/${c}/${c}-sym.json`, 'utf-8');
      const ref_data = await readFile(`${process.cwd()}/tests/pysonar2/${g}/${c}/${c}-ref.json`, 'utf-8');

      if (sym_data && ref_data) {
        // console.log(data.replaceAll(/\s+/g, ' '));
        builder(sym_data, ref_data, g, c);
        return UNIMatcher(cs, 'python', 'pysonar2');
      } else {
        error(`Failed to read pysonar2 output on ${g}/${c}`);
      }
    } else {
      error(`Failed to execute pysonar2 on ${g}/${c}`);
    }
  }
};
