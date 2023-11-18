import exec from '../../../common/exec';
import {mkdir} from 'fs/promises';

export default async (g: string, c: string, exepath: string) => {
  const ocwd = process.cwd();
  await mkdir(ocwd + `/tests/pysonar2/${g}/${c}`, {recursive: true});
  process.chdir(ocwd + `/tests/pysonar2/${g}/${c}`);
  try {
    let cmd = `java -classpath ${exepath} org.yinwang.pysonar.JSONDump ${ocwd}\\tests\\cases\\_${g}\\_${c} : ${c}`;
    await exec(cmd);

  } catch {
    return false;
  } finally {
    process.chdir(ocwd);
  }

  return true;
};
