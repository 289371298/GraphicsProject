[X,Y,Z]=textread('C:\Users\Administrator\PycharmProjects\Graphi\venv\test_on_629_night\corre.txt','%f %f %f');
A=sparse(X,Y,Z);
[r,g,b,x,y,z]=textread('C:\Users\Administrator\PycharmProjects\Graphi\venv\test_on_629_night\const.txt','%f %f %f %f %f %f');
solr=gmres(A,r,[],[],10000);
solg=gmres(A,g,[],[],10000);
solb=gmres(A,b,[],[],10000);
solx=gmres(A,x,[],[],10000);
soly=gmres(A,y,[],[],10000);
solz=gmres(A,z,[],[],10000);
fid1=fopen('C:\Users\Administrator\PycharmProjects\Graphi\venv\test_on_629_night\result.txt','w')
ans=[solx,soly,solz,solr,solg,solb]
fprintf(fid1,'%f %f %f %f %f %f\n',[solx,soly,solz,solr,solg,solb]');