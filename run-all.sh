

for OPT in semantic levenshtein tree_diff ; do
  for ASN in Docdiff Nile Filesystem ; do
    docker run --rm -it sidprasad/wfe-clustering ${OPT} ${ASN} >& wfe-clustering-${OPT}-${ASN}.txt
  done
done

for ASN in DocDiff Nile Filesystem ; do
  docker run --rm -it sidprasad/fv-eval:latest ${ASN} >& fv-eval-${ASN}.txt
done

for ASN in DocDiff Nile Filesystem ; do
  docker run --rm -it sidprasad/chaff-eval:latest ${ASN} >& chaff-eval-${ASN}.txt
done
