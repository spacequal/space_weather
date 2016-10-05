function fcheck, p1, p2
;
;if (n_elements(p2) ne 0) then if (p1 ne p2) then begin
;    print, 'FCHECK: p1 ne p2'
;    print, 'p1 = ', p1
;    print, 'p2 = ', p2
;end
;
out = 0
if (n_elements(p2) ne 0) then out = p2
if (n_elements(p1) ne 0) then out = p1
return, out
end
